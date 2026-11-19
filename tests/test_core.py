"""Network-free tests for the pure parts of ytkit. Run: python -m unittest discover tests"""

import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "ultimate-youtube" / "scripts"
sys.path.insert(0, str(ROOT))
os.environ["YT_SKILL_HOME"] = tempfile.mkdtemp(prefix="yt-skill-test-")

from ytkit import analysis, ids, quota, seo, transcript, util  # noqa: E402


def vid(i, views, days_ago, dur=600, title="Video"):
    published = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    return analysis.enrich({"video_id": f"id{i:09d}", "title": title, "views": views, "likes": views // 20,
                            "comments": views // 200, "published_at": published, "duration_s": dur, "tags": []}, 10_000)


class TestIds(unittest.TestCase):
    def test_video_ids(self):
        for raw in ["dQw4w9WgXcQ", "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10",
                    "youtu.be/dQw4w9WgXcQ", "https://youtube.com/shorts/dQw4w9WgXcQ?feature=share",
                    "https://www.youtube.com/live/dQw4w9WgXcQ", "https://www.youtube.com/embed/dQw4w9WgXcQ"]:
            self.assertEqual(ids.video_id(raw), "dQw4w9WgXcQ", raw)
        with self.assertRaises(ValueError):
            ids.video_id("not a video")

    def test_channel_refs(self):
        self.assertEqual(ids.channel_ref("UC" + "a" * 22), {"id": "UC" + "a" * 22})
        self.assertEqual(ids.channel_ref("@creator"), {"handle": "@creator"})
        self.assertEqual(ids.channel_ref("https://www.youtube.com/@creator/videos"), {"handle": "@creator"})
        self.assertEqual(ids.channel_ref("https://youtube.com/user/oldname"), {"username": "oldname"})
        self.assertEqual(ids.channel_ref("some channel name"), {"query": "some channel name"})
        self.assertEqual(ids.uploads_playlist("UCabc"), "UUabc")


class TestUtil(unittest.TestCase):
    def test_duration(self):
        self.assertEqual(util.iso_duration_seconds("PT1H2M3S"), 3723)
        self.assertEqual(util.iso_duration_seconds("PT45S"), 45)
        self.assertEqual(util.iso_duration_seconds("P1DT1S"), 86401)
        self.assertEqual(util.iso_duration_seconds(None), 0)
        self.assertEqual(util.hms(3723), "1:02:03")
        self.assertEqual(util.hms(65), "1:05")

    def test_human(self):
        self.assertEqual(util.human(1_500_000), "1.5M")
        self.assertEqual(util.human(950), "950")


class TestAnalysis(unittest.TestCase):
    def test_outlier_detection(self):
        vids = [vid(i, 1000, 100 - i * 5) for i in range(15)]
        vids.append(vid(99, 9000, 20, title="The Big One"))
        scored = analysis.score_outliers(vids)
        hit = next(v for v in scored if v["video_id"] == "id000000099")
        self.assertTrue(hit["is_outlier"])
        self.assertGreaterEqual(hit["neighbour_ratio"], 8)
        self.assertEqual(sum(v["is_outlier"] for v in scored), 1)

    def test_formats_compared_separately(self):
        longs = [vid(i, 1000, 50 + i) for i in range(8)]
        shorts = [vid(100 + i, 50_000, 50 + i, dur=40) for i in range(8)]
        scored = analysis.score_outliers(longs + shorts)
        self.assertFalse(any(v["is_outlier"] for v in scored))
        split = analysis.format_split(scored)
        self.assertEqual(split["short"]["count"], 8)
        self.assertEqual(split["long"]["median_views"], 1000)

    def test_fresh_videos_not_flagged(self):
        vids = [vid(i, 1000, 30 + i) for i in range(10)] + [vid(50, 9000, 1)]
        scored = analysis.score_outliers(vids)
        self.assertFalse(next(v for v in scored if v["video_id"] == "id000000050")["is_outlier"])

    def test_cadence(self):
        vids = [vid(i, 100, i * 7) for i in range(10)]
        c = analysis.cadence(vids)
        self.assertAlmostEqual(c["uploads_per_week"], 1.11, places=1)
        self.assertAlmostEqual(c["median_gap_days"], 7, delta=0.1)

    def test_tokens_any_script(self):
        toks = analysis.tokens("Why did this happen? | कहानी का सच — part 2")
        self.assertIn("कहानी", toks)
        self.assertIn("happen", toks)
        self.assertNotIn("2", toks)

    def test_title_features(self):
        f = analysis.title_features("7 Mistakes You Make Every Day?!")
        self.assertTrue(f["starts_with_number"] and f["has_question"] and f["addresses_viewer"])

    def test_comment_categories(self):
        self.assertIn("request", analysis.categorize_comment("Please make a video on part 2!"))
        self.assertIn("question", analysis.categorize_comment("How did you do that?"))
        self.assertIn("timestamp", analysis.categorize_comment("3:45 was the best moment"))
        self.assertEqual(analysis.categorize_comment("ok"), ["general"])

    def test_early_performance(self):
        peers = [vid(i, 1000, 30 + i) for i in range(10)]
        fresh = vid(77, 1500, 1)
        e = analysis.early_performance(fresh, peers + [fresh])
        self.assertEqual(e["pct_of_typical"], 150)

    def test_velocity(self):
        self.assertEqual(analysis.velocity([("2026-01-01T00:00:00+00:00", 100), ("2026-01-01T10:00:00+00:00", 600)]), 50.0)
        self.assertIsNone(analysis.velocity([("2026-01-01T00:00:00+00:00", 100)]))


class TestSeo(unittest.TestCase):
    def test_limits(self):
        r = seo.lint("x" * 101, "<b>", ["a"] * 3)
        self.assertGreaterEqual(r["errors"], 2)

    def test_chapters(self):
        good = "Intro\n0:00 Start\n1:00 Middle\n2:30 End"
        self.assertEqual(seo.check_chapters(seo.parse_chapters(good), 300), [])
        bad = "0:05 Start\n0:10 Too soon"
        issues = seo.check_chapters(seo.parse_chapters(bad))
        self.assertTrue(any("0:00" in i for i in issues))
        self.assertTrue(any("at least 3" in i for i in issues))

    def test_hashtags(self):
        desc = " ".join(f"#tag{i}" for i in range(16))
        self.assertTrue(any("ignores ALL" in i for i in seo.lint("Fine title for testing", desc)["issues"]))

    def test_clean_metadata_scores_high(self):
        desc = "How to bake sourdough bread at home, step by step. " * 6 + "\n0:00 Intro\n1:00 Dough\n5:00 Bake"
        r = seo.lint("How to Bake Sourdough Bread at Home", desc, ["sourdough", "bread"], "sourdough", 600)
        self.assertEqual(r["errors"], 0)
        self.assertGreaterEqual(r["score"], 90)


class TestTranscriptParsing(unittest.TestCase):
    def test_vtt_rolling_duplicates(self):
        vtt = """WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000
hello there

00:00:02.000 --> 00:00:04.000
hello there <c>general</c> kenobi

00:00:04.000 --> 00:00:06.000
general kenobi
"""
        segs = transcript.parse_vtt(vtt)
        self.assertEqual(segs[0]["text"], "hello there")
        self.assertEqual(segs[1]["text"], "general kenobi")
        self.assertEqual(segs[1]["start"], 2.0)

    def test_srt(self):
        srt = "1\n00:00:01,000 --> 00:00:02,500\nFirst line\n\n2\n00:01:00,000 --> 00:01:02,000\nSecond"
        segs = transcript.parse_vtt(srt)
        self.assertEqual([s["text"] for s in segs], ["First line", "Second"])
        self.assertEqual(segs[1]["start"], 60.0)


class TestQuota(unittest.TestCase):
    def test_buckets(self):
        quota.reset()
        quota.record("search.list", 3)
        quota.record("videos.update", 2)
        quota.record("videos.insert")
        st = quota.status()["buckets"]
        self.assertEqual(st["search"]["used"], 3)
        self.assertEqual(st["units"]["used"], 100)
        self.assertEqual(st["upload"]["used"], 1)
        ok, _ = quota.can_afford("captions.insert", 30)
        self.assertFalse(ok)
        self.assertEqual(quota.estimate({"videos.list": 4, "search.list": 2}), {"units": 4, "search": 2})


if __name__ == "__main__":
    unittest.main()
