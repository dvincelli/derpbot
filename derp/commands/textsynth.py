import requests
import os


class TextSynthCommand:
    command = "textsynth"
    engines = [
        "gptj_6B",
        "boris_6B",
        "fairseq_gpt_13B",
        "gptneox_20B",
        "flan_t5_xxl",
        "codegen_6B_mono",
        "m2m100_1_2B",
        "stable_diffusion",
    ]
    url = "https://api.textsynth.com/v1/engines/{engine_id}/completions"
    wants_parse = True

    def __call__(self, command):
        (_, command, args) = command
        api_key = os.getenv("TEXTSYNTH_API_KEY")
        engine_id = args.get("engine", "fairseq_gpt_13B")
        max_tokens = args.get("max_tokens", 50)
        response = requests.post(
            self.url.format(engine_id=engine_id),
            json={"prompt": args["prompt"], "max_tokens": max_tokens},
            headers={"Authorization": f"Bearer {api_key}"},
        )
        return response.json()["text"]
