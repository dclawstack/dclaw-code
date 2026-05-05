"use client";

import { useState } from "react";
import { sendChatMessage, codeCompletion } from "@/lib/api";
import type { CodeCompletionResponse, ChatMessageResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import { MessageSquareCode, Send, User, Bot, Copy } from "lucide-react";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  isCode?: boolean;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      let response = "";
      // Check if this is a code completion request
      if (userMsg.toLowerCase().includes("complete") || userMsg.toLowerCase().includes("write code") || userMsg.toLowerCase().includes("function")) {
        const res = await codeCompletion({ prompt: userMsg, language: "python" });
        response = res.completion;
      } else {
        const res = await sendChatMessage({ role: "user", content: userMsg });
        response = res.content;
      }
      setMessages((prev) => [...prev, { role: "assistant", content: response, isCode: true }]);
    } catch (err) {
      toast.error("Failed", { description: err instanceof Error ? err.message : "" });
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I encountered an error. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  function copyCode(content: string) {
    navigator.clipboard.writeText(content);
    toast.success("Copied");
  }

  return (
    <div className="space-y-4 max-w-4xl mx-auto h-[calc(100vh-140px)] flex flex-col">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          <MessageSquareCode className="w-6 h-6 text-primary" />
          AI Chat
        </h1>
        <p className="text-muted-foreground">Code-focused chat with AI assistance.</p>
      </div>

      <ScrollArea className="flex-1 border rounded-lg p-4 bg-card">
        {messages.length === 0 ? (
          <div className="text-center text-muted-foreground py-20">
            <Bot className="w-10 h-10 mx-auto mb-3 opacity-50" />
            <p className="text-sm">Start a conversation about code.</p>
            <p className="text-xs mt-1">Try: &quot;Write a function to sort a list&quot; or &quot;Explain quicksort&quot;</p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}>
                {msg.role === "assistant" && (
                  <div className="w-7 h-7 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                    <Bot className="w-4 h-4 text-primary" />
                  </div>
                )}
                <Card className={`max-w-[80%] ${msg.role === "user" ? "bg-primary text-primary-foreground" : ""}`}>
                  <CardContent className="p-3">
                    {msg.isCode ? (
                      <div className="space-y-2">
                        <pre className="font-mono text-sm whitespace-pre-wrap">{msg.content}</pre>
                        <Button variant="ghost" size="sm" className="h-6 text-xs" onClick={() => copyCode(msg.content)}>
                          <Copy className="w-3 h-3 mr-1" /> Copy
                        </Button>
                      </div>
                    ) : (
                      <p className="text-sm">{msg.content}</p>
                    )}
                  </CardContent>
                </Card>
                {msg.role === "user" && (
                  <div className="w-7 h-7 rounded-full bg-muted flex items-center justify-center shrink-0">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex gap-3">
                <div className="w-7 h-7 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 text-primary animate-pulse" />
                </div>
                <Badge variant="secondary">Thinking...</Badge>
              </div>
            )}
          </div>
        )}
      </ScrollArea>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about code..."
          className="min-h-[60px] resize-none"
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />
        <Button type="submit" disabled={loading || !input.trim()} className="self-end">
          <Send className="w-4 h-4" />
        </Button>
      </form>
    </div>
  );
}
