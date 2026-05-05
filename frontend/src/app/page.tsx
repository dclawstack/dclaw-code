"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import Link from "next/link";
import { listProjects, ProjectResponse } from "@/lib/api";
import {
  Code2,
  FolderGit2,
  MessageSquareCode,
  Rocket,
  Sparkles,
  Zap,
} from "lucide-react";

export default function DashboardPage() {
  const [projects, setProjects] = useState<ProjectResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listProjects()
      .then(setProjects)
      .catch((err) => toast.error("Failed to load projects", { description: err.message }))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-primary" />
          DClaw Code
        </h1>
        <p className="text-muted-foreground">AI-native IDE inside your desktop</p>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <FolderGit2 className="w-4 h-4 text-primary" />
              Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : projects.length}</div>
            <p className="text-xs text-muted-foreground mt-1">Total</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Code2 className="w-4 h-4 text-primary" />
              Files
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">—</div>
            <p className="text-xs text-muted-foreground mt-1">Tracked</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <MessageSquareCode className="w-4 h-4 text-primary" />
              Messages
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">—</div>
            <p className="text-xs text-muted-foreground mt-1">Chat history</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Zap className="w-4 h-4 text-primary" />
              Completions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">—</div>
            <p className="text-xs text-muted-foreground mt-1">AI generated</p>
          </CardContent>
        </Card>
      </div>

      <Separator />

      <div className="space-y-3">
        <h2 className="text-lg font-semibold">Quick Actions</h2>
        <div className="flex flex-wrap gap-3">
          <Link href="/editor">
            <Button><Code2 className="w-4 h-4 mr-2" />Open Editor</Button>
          </Link>
          <Link href="/chat">
            <Button variant="outline"><MessageSquareCode className="w-4 h-4 mr-2" />AI Chat</Button>
          </Link>
          <Link href="/projects">
            <Button variant="outline"><FolderGit2 className="w-4 h-4 mr-2" />Projects</Button>
          </Link>
        </div>
      </div>

      <Card>
        <CardHeader><CardTitle className="text-sm">Recent Projects</CardTitle></CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2">
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-8 w-full" />
            </div>
          ) : projects.length === 0 ? (
            <p className="text-sm text-muted-foreground">No projects yet. Create your first project to get started.</p>
          ) : (
            <div className="space-y-2">
              {projects.slice(0, 5).map((p) => (
                <div key={p.id} className="flex items-center justify-between py-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary">{p.language || "unknown"}</Badge>
                    <span className="text-sm font-medium">{p.name}</span>
                    <span className="text-xs text-muted-foreground">{p.git_branch}</span>
                  </div>
                  <Link href="/projects"><Button variant="ghost" size="sm">View</Button></Link>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle className="text-sm">System Status</CardTitle></CardHeader>
        <CardContent className="space-y-2 text-sm">
          <div className="flex justify-between"><span className="text-muted-foreground">Backend API</span><Badge variant="secondary">Port 8094</Badge></div>
          <div className="flex justify-between"><span className="text-muted-foreground">Frontend</span><Badge variant="secondary">Port 3005</Badge></div>
          <div className="flex justify-between"><span className="text-muted-foreground">Database</span><Badge variant="secondary">PostgreSQL 16</Badge></div>
          <div className="flex justify-between"><span className="text-muted-foreground">LLM</span><Badge variant="secondary">Ollama / OpenRouter</Badge></div>
        </CardContent>
      </Card>
    </div>
  );
}
