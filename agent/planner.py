from agent.llm import llm
from agent.traces import log

class Planner:
    def create_plan(self, prompt):
        log("planner_start", {"prompt": prompt})
        # Demo ke liye auto-resolve
        if "analytics" in prompt.lower() and "code" not in prompt.lower() and "all" not in prompt.lower():
            prompt = prompt + " per code"
            log("ambiguity_auto_resolved", {"assumption": "per code analytics"})

        res = llm.call(f"You are Planner. Break this into tasks: {prompt}", "reasoning")
        plan = {"tasks": res["tasks"], "risks": res.get("risks", []), "mitigations": res.get("mitigations", [])}
        plan["needs_clarification"] = False 
        log("planner_done", plan)
        return plan