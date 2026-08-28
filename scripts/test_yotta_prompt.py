#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta-prompt（元引）单元测试。

运行（在技能目录内）：python scripts/test_yotta_prompt.py
或（仓库根）：python yottaskills/yotta-prompt/scripts/test_yotta_prompt.py
"""

import json
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yotta_prompt as yp

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yotta_prompt.py")


def run_cli(*args):
    """以子进程方式运行 CLI（Windows 下也保证 UTF-8 输出）。"""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, SCRIPT] + list(args),
        capture_output=True, encoding="utf-8", errors="replace", env=env,
    )


def top_domain(text):
    return yp.candidates_for(text)[0]["id"]


class TestClarifyIntent(unittest.TestCase):
    def test_writing_intent_top(self):
        self.assertEqual(top_domain("帮我写一封邮件给客户"), "writing")

    def test_memory_intent_top(self):
        self.assertEqual(top_domain("帮我记住这个地址"), "memory")

    def test_security_intent_top(self):
        self.assertEqual(top_domain("看看项目里有没有密钥泄露"), "security")

    def test_dev_intent_top(self):
        self.assertEqual(top_domain("这段代码为什么报错"), "dev")

    def test_logs_intent_top(self):
        self.assertEqual(top_domain("查一下日志里的报错"), "logs")

    def test_learning_intent_top(self):
        self.assertEqual(top_domain("想入门机器学习"), "learning")

    def test_quality_intent_top(self):
        self.assertEqual(top_domain("认真点，别敷衍"), "quality")

    def test_analysis_intent_top(self):
        self.assertEqual(top_domain("帮我整理数据做个表格"), "analysis")

    def test_planning_intent_top(self):
        self.assertEqual(top_domain("帮我制定一个项目计划"), "planning")

    def test_skill_alias_cn_pins_domain(self):
        cands = yp.candidates_for("元忆怎么用")
        self.assertEqual(cands[0]["id"], "memory")
        self.assertIn("元忆", cands[0]["reason"])

    def test_skill_alias_slug_pins_domain(self):
        cands = yp.candidates_for("yotta-memory 能干嘛")
        self.assertEqual(cands[0]["id"], "memory")

    def test_mixed_input_has_multiple_candidates(self):
        cands = yp.candidates_for("写代码的时候顺便帮我记住要点")
        ids = [c["id"] for c in cands]
        self.assertIn("dev", ids)
        self.assertIn("memory", ids)
        self.assertGreaterEqual(len(cands), 2)
        self.assertLessEqual(len(cands), 4)

    def test_general_padding_when_single_match(self):
        cands = yp.candidates_for("帮我写封邮件")
        self.assertGreaterEqual(len(cands), 2)
        self.assertTrue(any(c["id"] == "general" for c in cands))

    def test_candidate_schema(self):
        cands = yp.candidates_for("帮我写封邮件")
        for c in cands:
            for key in ("id", "label_zh", "label_en", "reason", "skills"):
                self.assertIn(key, c)


class TestClarifyCLI(unittest.TestCase):
    def test_recognized_exit0(self):
        r = run_cli("clarify", "帮我写一封邮件")
        self.assertEqual(r.returncode, 0)
        self.assertIn("写作与语言", r.stdout)

    def test_unrecognized_exit1(self):
        r = run_cli("clarify", "你好呀")
        self.assertEqual(r.returncode, 1)
        self.assertIn("没能识别出", r.stdout)

    def test_empty_input_exit4(self):
        r = run_cli("clarify", "")
        self.assertEqual(r.returncode, 4)

    def test_missing_arg_exit4(self):
        r = run_cli("clarify")
        self.assertEqual(r.returncode, 4)

    def test_short_input_exit1(self):
        r = run_cli("clarify", "的")
        self.assertEqual(r.returncode, 1)

    def test_json_recognized(self):
        r = run_cli("clarify", "看看有没有密钥", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertTrue(data["recognized"])
        self.assertEqual(data["candidates"][0]["id"], "security")

    def test_json_unrecognized(self):
        r = run_cli("clarify", "哈哈", "--json")
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        self.assertFalse(data["recognized"])

    def test_top_limit(self):
        r = run_cli("clarify", "写代码修 bug 记笔记查日志", "--top", "2", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertLessEqual(len(data["candidates"]), 2)

    def test_lang_en(self):
        r = run_cli("clarify", "帮我写一封邮件", "--lang", "en")
        self.assertIn("Writing & Language", r.stdout)


class TestMap(unittest.TestCase):
    def test_map_domain_zh(self):
        res = yp.map_result("写作")
        self.assertIsNotNone(res)
        self.assertEqual(res["domain"]["id"], "writing")
        slugs = [s["slug"] for s in res["skills"]]
        self.assertIn("yotta-humanize", slugs)
        self.assertTrue(res["prompt"])

    def test_map_domain_en(self):
        self.assertEqual(yp.map_result("writing")["domain"]["id"], "writing")

    def test_map_domain_id(self):
        self.assertEqual(yp.map_result("security")["domain"]["id"], "security")

    def test_map_skill_slug(self):
        res = yp.map_result("yotta-humanize")
        self.assertEqual(res["kind"], "skill")
        self.assertEqual(res["skills"][0]["slug"], "yotta-humanize")

    def test_map_skill_cn(self):
        res = yp.map_result("元钥")
        self.assertEqual(res["skills"][0]["slug"], "yotta-secret")

    def test_map_skill_cn_short(self):
        res = yp.map_result("元忆")
        self.assertEqual(res["skills"][0]["slug"], "yotta-memory")

    def test_map_by_keyword(self):
        res = yp.map_result("密钥")
        self.assertEqual(res["domain"]["id"], "security")

    def test_map_miss_none(self):
        self.assertIsNone(yp.map_result("asdfqwerzx"))

    def test_map_miss_exit1(self):
        r = run_cli("map", "asdfqwerzx")
        self.assertEqual(r.returncode, 1)

    def test_map_empty_exit4(self):
        r = run_cli("map", "")
        self.assertEqual(r.returncode, 4)

    def test_map_json(self):
        r = run_cli("map", "写作", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertTrue(data["found"])
        self.assertIn("prompt", data)
        for s in data["skills"]:
            self.assertTrue(s["install"].startswith("npx -y @yottameta/"))

    def test_map_all_skills_have_install(self):
        for slug, info in yp.SKILLS.items():
            self.assertTrue(info["tagline"])
            self.assertIn(info["domain"], yp.DOMAIN_BY_ID)


class TestScenarios(unittest.TestCase):
    def test_scenarios_count(self):
        self.assertGreaterEqual(len(yp.SCENARIOS), 15)
        # 行业无关：必须包含非技术 / 非安全场景
        titles = " ".join(sc["title"] for sc in yp.SCENARIOS)
        for kw in ("周报", "表格", "演讲稿", "翻译", "会议纪要", "合同", "面试"):
            self.assertIn(kw, titles)

    def test_scenarios_cli(self):
        r = run_cli("scenarios")
        self.assertEqual(r.returncode, 0)
        self.assertIn("写一封邮件", r.stdout)

    def test_scenarios_json(self):
        r = run_cli("scenarios", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        for sc in data:
            for key in ("id", "title", "input", "domain"):
                self.assertIn(key, sc)


class TestMisc(unittest.TestCase):
    def test_version(self):
        r = run_cli("--version")
        self.assertEqual(r.returncode, 0)
        self.assertIn("0.1.0", r.stdout)

    def test_no_command_exit4(self):
        r = run_cli()
        self.assertEqual(r.returncode, 4)

    def test_unknown_command_exit4(self):
        r = run_cli("bogus")
        self.assertEqual(r.returncode, 4)

    def test_domains_consistent(self):
        ids = [d["id"] for d in yp.DOMAINS]
        self.assertEqual(len(ids), len(set(ids)))
        for d in yp.DOMAINS:
            for slug in d["skills"]:
                self.assertIn(slug, yp.SKILLS)

    def test_skill_alias_consistent(self):
        for alias, dom in yp.SKILL_ALIAS.items():
            self.assertIn(dom, yp.DOMAIN_BY_ID)


class TestPromptsSelfSufficient(unittest.TestCase):
    def test_every_prompt_has_fallback_hint(self):
        # 每个提示词都必须自包含：目标技能未安装也能直接运行
        # 有专属技能的域要求含「若已安装」增强句；无专属技能域（general/analysis/planning）天然自包含
        for dom_id, prompt in yp.PROMPTS.items():
            self.assertTrue(prompt.strip(), dom_id)
            if yp.DOMAIN_BY_ID[dom_id]["skills"]:
                self.assertIn("若已安装", prompt, dom_id)
            else:
                self.assertIn("请", prompt, dom_id)

    def test_map_prompt_self_sufficient(self):
        res = yp.map_result("写作")
        self.assertIn("若已安装", res["prompt"])

    def test_map_skills_are_optional(self):
        r = run_cli("map", "写作")
        self.assertEqual(r.returncode, 0)
        self.assertIn("可选加速器", r.stdout)

    def test_map_analysis_domain(self):
        self.assertEqual(yp.map_result("数据")["domain"]["id"], "analysis")

    def test_map_planning_domain(self):
        self.assertEqual(yp.map_result("计划")["domain"]["id"], "planning")

    def test_domains_include_industry_agnostic(self):
        ids = [d["id"] for d in yp.DOMAINS]
        self.assertIn("analysis", ids)
        self.assertIn("planning", ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)
