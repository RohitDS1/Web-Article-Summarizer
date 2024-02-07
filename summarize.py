from transformers import AutoModelWithLMHead, AutoTokenizer

class Summarizer():
    """
    This Summarizer class utilizes the T5 (Text-to-Text Transfer Transformer) model that has been specifically
    fine-tuned on a News Summary dataset for the purpose of summarizing textual data.

    About the Model:
    - Model Name: "t5-base-finetuned-summarize-news"
    - Origin: The base model is Google's T5, which is designed as a unified transformer architecture capable 
      of converting every language problem into a text-to-text format.
    
    How It Works:
    - This class initializes with the specific tokenizer and model from the mentioned pretrained version.
    - The T5 framework views every NLP task as a text-to-text problem, thereby allowing for seamless 
      transfer learning across diverse NLP tasks.
    
    Why Use This Model:
    - Transfer Learning: T5 is based on the principle of transfer learning where a model is pre-trained on a 
      data-rich task and then fine-tuned for specific downstream tasks. This method has proven to be highly 
      effective in NLP.
    - State-of-the-Art Results: As per the original paper "Exploring the Limits of Transfer Learning with a Unified
      Text-to-Text Transformer", combining T5 with large-scale datasets (like the "Colossal Clean Crawled Corpus") 
      achieves state-of-the-art results on multiple NLP benchmarks including summarization, question answering, 
      text classification, etc.
    - Adaptability: The unified text-to-text framework of T5 makes it adaptable to a wide range of NLP tasks with 
      minimal changes.
    
    Reference:
    Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, 
    Peter J. Liu. "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer".
    """
        
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
        self.model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")

    def summarize(self, text, max_length=150):
        input_ids = self.tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
        generated_ids = self.model.generate(input_ids=input_ids, num_beams=2, max_length=max_length,  repetition_penalty=2.5, length_penalty=1.0, early_stopping=True)
        preds = [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
        # Capitalize the first letter in each sentence.
        sentences = preds[0].split('. ')
        capitalized_sentences = [s[0].upper() + s[1:] if s else "" for s in sentences]
        capitalized_text = '. '.join(capitalized_sentences)
        if capitalized_text and not capitalized_text.endswith('.'):
            capitalized_text += '.'
        return capitalized_text
