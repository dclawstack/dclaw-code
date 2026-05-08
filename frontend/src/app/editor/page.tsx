"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";
import { codeCompletion, codeRefactor, codeExplain, codeGenerateTests } from "@/lib/api";
import type { CodeCompletionResponse, CodeRefactorResponse, CodeExplainResponse, CodeGenerateTestsResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { Code2, Sparkles, Wrench, BookOpen, FlaskConical, Copy } from "lucide-react";

type ToolResult =
  | { type: "completion"; data: CodeCompletionResponse }
  | { type: "refactor"; data: CodeRefactorResponse }
  | { type: "explain"; data: CodeExplainResponse }
  | { type: "tests"; data: CodeGenerateTestsResponse }
  | null;

const LANGUAGE_MAP: Record<string, string> = {
  python: "python",
  typescript: "typescript",
  javascript: "javascript",
  rust: "rust",
  go: "go",
};

export default function EditorPage() {
  const [code, setCode] = useState("def process_data(data):\n    result = []\n    for item in data:\n        if item.get('active'):\n            result.append({**item, 'processed': True})\n    return result");
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ToolResult>(null);

  async function handleComplete() {
    setLoading(true);
    try {
      const res = await codeCompletion({ prompt: code, language });
      setResult({ type: "completion", data: res });
      toast.success("Completion generated");
    } catch (err) {
      toast.error("Failed", { description: err instanceof Error ? err.message : "" });
    } finally { setLoading(false); }
  }

  async function handleRefactor() {
    setLoading(true);
    try {
      const res = await codeRefactor({ code, language, goal: "improve readability" });
      setResult({ type: "refactor", data: res });
      toast.success("Refactored");
    } catch (err) {
      toast.error("Failed", { description: err instanceof Error ? err.message : "" });
    } finally { setLoading(false); }
  }

  async function handleExplain() {
    setLoading(true);
    try {
      const res = await codeExplain({ code, language, detail_level: "medium" });
      setResult({ type: "explain", data: res });
      toast.success("Explanation generated");
    } catch (err) {
      toast.error("Failed", { description: err instanceof Error ? err.message : "" });
    } finally { setLoading(false); }
  }

  async function handleTests() {
    setLoading(true);
    try {
      const res = await codeGenerateTests({ code, language, framework: "pytest" });
      setResult({ type: "tests", data: res });
      toast.success("Tests generated", { description: `${res.test_cases_count} test cases` });
    } catch (err) {
      toast.error("Failed", { description: err instanceof Error ? err.message : "" });
    } finally { setLoading(false); }
  }

  function copyResult() {
    let text = "";
    if (result?.type === "completion") text = result.data.completion;
    else if (result?.type === "refactor") text = result.data.refactored_code;
    else if (result?.type === "explain") text = result.data.explanation;
    else if (result?.type === "tests") text = result.data.test_code;
    if (text) { navigator.clipboard.writeText(text); toast.success("Copied"); }
  }

  return (
    <div className="space-y-4 max-w-6xl mx-auto">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          <Code2 className="w-6 h-6 text-primary" />
          Editor
        </h1>
        <p className="text-muted-foreground">Write code and use AI tools from the sidebar.</p>
      </div>

      <div className="flex gap-3 items-center">
        <Select value={language} onValueChange={(v) => setLanguage(v ?? "python")}>
          <SelectTrigger className="w-[140px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="python">Python</SelectItem>
            <SelectItem value="typescript">TypeScript</SelectItem>
            <SelectItem value="javascript">JavaScript</SelectItem>
            <SelectItem value="rust">Rust</SelectItem>
            <SelectItem value="go">Go</SelectItem>
          </SelectContent>
        </Select>
        <div className="flex gap-2 ml-auto">
          <Button size="sm" onClick={handleComplete} disabled={loading || !code.trim()}>
            <Sparkles className="w-4 h-4 mr-1" /> Complete
          </Button>
          <Button size="sm" variant="outline" onClick={handleRefactor} disabled={loading || !code.trim()}>
            <Wrench className="w-4 h-4 mr-1" /> Refactor
          </Button>
          <Button size="sm" variant="outline" onClick={handleExplain} disabled={loading || !code.trim()}>
            <BookOpen className="w-4 h-4 mr-1" /> Explain
          </Button>
          <Button size="sm" variant="outline" onClick={handleTests} disabled={loading || !code.trim()}>
            <FlaskConical className="w-4 h-4 mr-1" /> Tests
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="min-h-[500px] overflow-hidden">
          <CardHeader className="pb-2"><CardTitle className="text-xs font-medium text-muted-foreground">Source Code</CardTitle></CardHeader>
          <CardContent className="p-0">
            <Editor
              height="460px"
              language={LANGUAGE_MAP[language] || "plaintext"}
              value={code}
              onChange={(v) => setCode(v ?? "")}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                wordWrap: "on",
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </CardContent>
        </Card>

        <Card className="min-h-[500px]">
          <CardHeader className="pb-2 flex flex-row items-center justify-between">
            <CardTitle className="text-xs font-medium text-muted-foreground">
              {result?.type === "completion" && "AI Completion"}
              {result?.type === "refactor" && "Refactored Code"}
              {result?.type === "explain" && "Explanation"}
              {result?.type === "tests" && "Generated Tests"}
              {!result && "AI Output"}
            </CardTitle>
            {result && <Button variant="ghost" size="sm" onClick={copyResult}><Copy className="w-3 h-3 mr-1" /> Copy</Button>}
          </CardHeader>
          <CardContent>
            {!result && (
              <div className="text-sm text-muted-foreground text-center py-20">
                Select an AI tool to generate output
              </div>
            )}
            {result?.type === "completion" && (
              <pre className="font-mono text-sm whitespace-pre-wrap">{result.data.completion}</pre>
            )}
            {result?.type === "refactor" && (
              <div className="space-y-3">
                <div className="flex flex-wrap gap-1">
                  {result.data.changes_made.map((c, i) => <Badge key={i} variant="secondary">{c}</Badge>)}
                </div>
                <pre className="font-mono text-sm whitespace-pre-wrap">{result.data.refactored_code}</pre>
              </div>
            )}
            {result?.type === "explain" && (
              <div className="space-y-3">
                <p className="text-sm leading-relaxed">{result.data.explanation}</p>
                <div className="flex flex-wrap gap-1">
                  {result.data.key_concepts.map((c, i) => <Badge key={i} variant="outline">{c}</Badge>)}
                </div>
              </div>
            )}
            {result?.type === "tests" && (
              <pre className="font-mono text-sm whitespace-pre-wrap">{result.data.test_code}</pre>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
