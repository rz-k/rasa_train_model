import json
import yaml




class Base:
    
    def __init__(self) -> None:
        self.file_path_counversiotion_json = "counversiotion.json"
        self.version = 'version: "3.1"\n\n'   

    def write_file(self, data, write_file_path):
        with open(write_file_path, "a") as file:
            file.write(data)

    def load_json_file(self):
        with open(self.file_path_counversiotion_json, encoding="utf-8") as file:
            data = json.load(file)
        return data    

class Domain(Base):
    def __init__(self) -> None:
        super().__init__()
        self.session_data = """session_config:\n  session_expiration_time: 1\n  carry_over_slots_to_new_session: false"""
        self.write_file_path = "domain.yml"

    def generate_intents(self, intents):
        temp_intent = ""
        for intent in intents:
            temp_intent+=f"  - {intent}\n"
        temp_intent = temp_intent + "  - nlu_fallback" + "\n"
        result = "intents:\n" + temp_intent + "\n"

        return result

    def generate_responses(self, responses, intent):
        tmp_response = ""
        for response in responses:
            tmp_response += f"   - text: {response}\n"
        return f"  utter_{intent}:\n" + tmp_response + "\n"

    def main(self):
        self.write_file(self.version, self.write_file_path) #write version
        intents = []
        
        for item in self.load_json_file():
            title = item.get("title")
            if not title:
                continue
            intents.append(title[0])
        
        self.write_file(self.generate_intents(intents), self.write_file_path) #write intents

        fallback = """
  utter_default:
    - text: "xxxxxxxxxxx"
  utter_fallback:
    - text: "xxxxxxxxxxx"
  utter_please_rephrase:
  - text: I'm sorry, I didn't quite understand that. Could you rephrase?        
"""
        temp_response_2 = ""
        for item in self.load_json_file():
            title = item.get("title")
            if not title:
                continue
            # titles = item.get("titles")
            answear = item.get("answear")
            result = self.generate_responses(answear, title[0])
            temp_response_2 += result
        self.write_file("responses:\n"+temp_response_2 + "\n", self.write_file_path)
        self.write_file(fallback, self.write_file_path)
        self.write_file(self.session_data, self.write_file_path)

class Nlu(Base):
    def __init__(self) -> None:
        super().__init__()
        self.write_file_path = "data/nlu.yml"

    def generate_examples(self, examples, intent):
        tmp_example = ""
        for example in examples:
            tmp_example += f"   - {example}\n"
        return f"- intent: {intent}\n  examples: |\n" + tmp_example + "\n"

    def main(self):
        self.write_file(self.version, self.write_file_path) #write version
        self.write_file("nlu:\n", self.write_file_path) #write nlu
        for item in self.load_json_file():
            title = item.get("title")
            if not title:
                continue
            result =self.generate_examples(item.get("titles"), item.get("title")[0])
            self.write_file(result, self.write_file_path)

class Rules(Base):
    def __init__(self) -> None:
        super().__init__()
        self.write_file_path = "data/rules.yml"

    def generate_steps(self, intent):
        tmp_step = f"  - rule: Say {intent}\n    steps:\n    - intent: {intent}\n    - action: utter_{intent}\n"
        return tmp_step

    def main(self):
        self.write_file(self.version, self.write_file_path) #write version
        self.write_file("rules:\n", self.write_file_path) #write - rules:

        fallback = """        
  - rule: Activate the fallback action when the user message is not understood
    steps:
      - intent: nlu_fallback
      - action: action_default_fallback
        """

        for item in self.load_json_file():
            title = item.get("title")
            if not title:
                continue

            result = self.generate_steps(item.get("title")[0])
            self.write_file(result + "\n", self.write_file_path)
        self.write_file(fallback, self.write_file_path)

class Stories(Base):
    def __init__(self) -> None:
        super().__init__()
        self.write_file_path = "data/stories.yml"

    def generate_steps(self, intent):
        tmp_step = f"- story: {intent}\n  steps:\n  - intent: {intent}\n  - action: utter_{intent}\n"
        return tmp_step

    def main(self):
        self.write_file(self.version, self.write_file_path) #write version
        self.write_file("stories:\n", self.write_file_path) #write stories

        for item in self.load_json_file():
            title = item.get("title")
            if not title:
                continue
            result = self.generate_steps(item.get("title")[0])
            self.write_file(result + "\n", self.write_file_path)


Rules().main()
Nlu().main()
Domain().main()
Stories().main()

exit()



# # Load JSON data
# with open('counversiotion.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)



# # # Generate nlu.yml
# nlu_data = {"version": "3.1"}
# x = []
# for item in data:
#     # print(item)
#     intent_name = item["title"][0]
#     # print([f"- {title}" for title in item["titles"]])
#     examples = "\n".join([f"- {title}" for title in item["titles"]])
#     print(examples)
#     print("="*100)
#     x.append({"intent": intent_name, "examples": examples})
#     nlu_data.update({"nlu": x})
# with open('data/nlu.yml', 'w', encoding='utf-8') as f:
#     yaml.dump(nlu_data, f, allow_unicode=True)

# # Generate nlu.yml
# # nlu_data = {"version": "3.1", "nlu": []}
# # for item in data:
# #     intent_name = item["title"][0]
# #     examples = "\n".join([f"- {title}" for title in item["titles"]])
# #     nlu_data["nlu"].append({"intent": intent_name, "examples": "|\n".replace("'", "") + examples})

# # with open('data/nlu.yml', 'w', encoding='utf-8') as f:
# #     yaml.dump(nlu_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)







# # Generate domain.yml
# domain_data = {
#     "version": "3.1",
#     "intents": [item["title"][0] for item in data],
#     "responses": {}
# }

# for item in data:
#     response_key = f"utter_{item['title'][0]}"
#     responses = [{"text": answer} for answer in item["answear"]]
#     domain_data["responses"][response_key] = responses

# with open('domain.yml', 'w', encoding='utf-8') as f:
#     yaml.dump(domain_data, f, allow_unicode=True)

# # Generate rules.yml
# rules_data = {"version": "3.1", "rules": []}

# for item in data:
#     intent_name = item["title"][0]
#     response_key = f"utter_{intent_name}"
#     rules_data["rules"].append({
#         "rule": f"پاسخ به {intent_name}",
#         "steps": [
#             {"intent": intent_name},
#             {"action": response_key}
#         ]
#     })

# with open('data/rules.yml', 'w', encoding='utf-8') as f:
#     yaml.dump(rules_data, f, allow_unicode=True)