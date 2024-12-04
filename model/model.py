"""
The `Model` class is an interface between the ML model that you're packaging and the model
server that you're running it on.

The main methods to implement here are:
* `load`: runs exactly once when the model server is spun up or patched and loads the
   model onto the model server. Include any logic for initializing your model, such
   as downloading model weights and loading the model into memory.
* `predict`: runs every time the model server is called. Include any logic for model
  inference and return the model output.

See https://truss.baseten.co/quickstart for more.
"""
from transformers import AutoTokenizer, AutoModelForCausalLM

class Model:
    def __init__(self, **kwargs):
        # self._data_dir = kwargs["data_dir"]
        # self._config = kwargs["config"]
        # self._secrets = kwargs["secrets"]
        self.tokenizer = None
        self._model = None


    def load(self):
        """
        Load the Qwen model and tokenizer.
        """
        model_id = "Qwen/Qwen2.5-3B"  # Hugging Face model ID
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self._model = AutoModelForCausalLM.from_pretrained(model_id)

        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_id}: {e}")


    def predict(self, model_input):
        """
        Run inference using the Qwen model.
        Args:
            model_input (dict): Should contain the key `text` with the prompt string.
        Returns:
            dict: Generated text from the model.
        """
        try:
            # Ensure `text` key exists in the input
            if "text" not in model_input:
                raise ValueError("Input dictionary must contain a `text` key.")

            input_text = model_input["text"]

            inputs = self.tokenizer.encode(
                input_text, return_tensors="pt", padding=True, truncation=True,)

            # Generate output using tokenized input
            outputs = self._model.generate(
                inputs,
                max_new_tokens=300,
                num_return_sequences=1,  # Change for multiple outputs
                temperature=0.7,
                top_p=0.9,  # Nucleus sampling, limits set of possible words
                do_sample=True,
            )

            # Decode the generated output
            result = self.tokenizer.decode(
                outputs[0], skip_special_tokens=True)
            return {"generated_text": result}

        except Exception as e:
            return {"error": str(e)}
