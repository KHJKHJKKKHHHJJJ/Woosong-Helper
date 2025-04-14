import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig

class LocalLLM:
    def __init__(self):
        # CPU 사용 (안정성을 위해)
        self.device = torch.device("cpu")
        
        # 기본 모델 ID
        self.base_model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        
        # 어댑터 경로 - 절대 경로로 변환
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.adapter_path = os.path.join(script_dir, "models", "final_lora_adapters")
        
        # 디렉토리 확인
        if not os.path.exists(self.adapter_path):
            os.makedirs(self.adapter_path, exist_ok=True)
            print(f"경고: 어댑터 경로가 존재하지 않아 생성했습니다: {self.adapter_path}")
            print("파인튜닝된 모델을 이 경로에 복사해야 합니다.")
        
        print(f"어댑터 경로: {self.adapter_path}")
        print(f"어댑터 파일 목록: {os.listdir(self.adapter_path) if os.path.exists(self.adapter_path) else '디렉토리가 비어있음'}")
        
        try:
            print("토크나이저 로딩 중...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_id)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("기본 모델 로딩 중...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.base_model_id,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            ).to(self.device)
            
            # 어댑터 설정 파일 확인
            config_path = os.path.join(self.adapter_path, "adapter_config.json")
            if os.path.exists(config_path):
                print("LoRA 어댑터 로딩 중...")
                # 어댑터 설정 먼저 로드
                peft_config = PeftConfig.from_pretrained(self.adapter_path)
                # 어댑터 로드
                self.model = PeftModel.from_pretrained(
                    self.model,
                    self.adapter_path,
                    config=peft_config
                )
                print("모델 로딩 완료!")
            else:
                print(f"경고: adapter_config.json 파일이 {self.adapter_path}에 없습니다.")
                print("기본 모델만 사용합니다.")
        except Exception as e:
            print(f"모델 로딩 중 오류 발생: {str(e)}")
            print("기본 모델만 사용합니다.")

    def generate_response(self, prompt, max_length=512):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # 입력 프롬프트 제거하여 실제 응답만 반환
            response = response[len(self.tokenizer.decode(inputs['input_ids'][0], skip_special_tokens=True)):].strip()
            return response
        except Exception as e:
            print(f"응답 생성 중 오류 발생: {str(e)}")
            return "죄송합니다. 응답 생성 중 오류가 발생했습니다."
