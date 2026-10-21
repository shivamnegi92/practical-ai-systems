import unittest
from unittest.mock import patch
from common.llm import OllamaLLM, OpenAICompatibleLLM

class ProviderTextContract(unittest.TestCase):
 def providers(self):
  return [(OllamaLLM("test"),lambda value:{"response":value}),(OpenAICompatibleLLM("test","http://example.invalid","test"),lambda value:{"choices":[{"message":{"content":value}}]})]
 def test_nontext_content_is_rejected_at_the_provider_boundary(self):
  for provider,wrap in self.providers():
   for value in (None,[],{},42,True):
    with self.subTest(provider=type(provider).__name__,value=value),patch.object(provider,"_post",return_value=wrap(value)),self.assertRaisesRegex(ValueError,"text"):
     provider.complete("Synthetic request")
 def test_text_is_preserved_including_empty_and_whitespace(self):
  for provider,wrap in self.providers():
   for value in ("","  answer  "):
    with self.subTest(provider=type(provider).__name__),patch.object(provider,"_post",return_value=wrap(value)):
     self.assertEqual(provider.complete("Synthetic request"),value)
