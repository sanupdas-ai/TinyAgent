class Memory:
  """Simple memory module to store conversation history."""
  
  def __init__(self):
    self.messages = []
    
  def add(
    self,
    role: str,
    content: str,
    tool_call: dict | None = None,
    **kwargs
  ) -> None:
    """Add a message to memory."""
    
    message = {"role": role, "content": content}
    
    if tool_call:
      message["tool_call"] = tool_call
    
    #message.update(kwargs)
    
    self.messages.append(message)
    
  def get_messages(self) -> list[dict]:
    """Get all messages."""
    return self.messages
  
class TrimmingMemory(Memory):
  """Memory that keeps only the last two user/assistant turns."""
  
  def add(
    self,
    role: str,
    content: str,
    **kwargs
  ) -> None:
    
    super().add(role, content, **kwargs)
    
    system = [
      message for message in self.messages if message["role"] == "system"
    ]
    
    turns = [
      message for message in self.messages if message["role"] != "system"
    ]
    
    self.messages = system + turns[-4:]  # Keep last 2 turns (4 messages) plus system messages
    
class SummarizationMemory(Memory):
  """Memory tha compresses past turns into a running summary via LLM."""
  
  def __init__(self, llm:LLM):
    super().__init__()
    self.llm = llm

  def add(
    self,
    role: str,
    content: str,
    **kwargs
  ) -> None:
    
    super().add(role, content, **kwargs)
    
    if role == "assistant":
      # Split existing summary from the new convesation turns
      summary = ""
      conversation = ""
      for message in self.messages:
        if message["role"] == "system":
          summary = message["content"]
        else:
          conversation += f"{message['role']}: {message['content']}\n"
          
      # Ask the llm to extend the summary with the new conversation
      prompt = f"""Update the summary with the new conversation.
Summary: {summary}

Conversation:
{conversation}
Output the updated summary only."""
      response = self.llm.generate([{"role": "user", "content": prompt}])
      self.messages = [{"role": "system", "content": response.content}]
        