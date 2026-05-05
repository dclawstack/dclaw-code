"use client";

import { useEffect, useState } from "react";
import {
  listProjects,
  createProject,
  ProjectResponse,
  ProjectCreate,
} from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { FolderGit2, Plus, GitBranch, FolderOpen } from "lucide-react";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<ProjectResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [language, setLanguage] = useState("python");
  const [repoUrl, setRepoUrl] = useState("");
  const [creating, setCreating] = useState(false);

  async function load() {
    setLoading(true);
    try { setProjects(await listProjects()); }
    catch (err) { toast.error("Failed", { description: err instanceof Error ? err.message : "" }); }
    finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;
    setCreating(true);
    try {
      const data: ProjectCreate = { name: name.trim(), description: description || undefined, language, repo_url: repoUrl || undefined };
      const created = await createProject(data);
      setProjects((prev) => [...prev, created]);
      toast.success("Project created", { description: created.name });
      setName(""); setDescription(""); setRepoUrl(""); setLanguage("python"); setDialogOpen(false);
    } catch (err) {
      toast.error("Failed", { description: err instanceof Error ? err.message : "" });
    } finally { setCreating(false); }
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <FolderGit2 className="w-6 h-6 text-primary" />
            Projects
          </h1>
          <p className="text-muted-foreground">Manage your code projects.</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger>
            <Button><Plus className="w-4 h-4 mr-2" />New Project</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create Project</DialogTitle>
              <DialogDescription>Set up a new project workspace.</DialogDescription>
            </DialogHeader>
            <form onSubmit={handleCreate} className="space-y-3 py-3">
              <div className="space-y-1"><Label htmlFor="p-name">Name</Label><Input id="p-name" value={name} onChange={(e) => setName(e.target.value)} placeholder="my-project" required /></div>
              <div className="space-y-1"><Label htmlFor="p-desc">Description</Label><Input id="p-desc" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Project description" /></div>
              <div className="space-y-1"><Label>Language</Label>
                <Select value={language} onValueChange={(v) => setLanguage(v ?? "python")}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="python">Python</SelectItem>
                    <SelectItem value="typescript">TypeScript</SelectItem>
                    <SelectItem value="rust">Rust</SelectItem>
                    <SelectItem value="go">Go</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1"><Label htmlFor="p-repo">Repo URL</Label><Input id="p-repo" value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} placeholder="https://github.com/..." /></div>
              <DialogFooter>
                <Button type="submit" disabled={creating}>{creating ? "Creating..." : "Create"}</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        {loading ? (
          <CardContent className="p-6 space-y-2"><Skeleton className="h-8 w-full" /><Skeleton className="h-8 w-full" /><Skeleton className="h-8 w-full" /></CardContent>
        ) : projects.length === 0 ? (
          <CardContent className="p-8 text-center space-y-3">
            <FolderOpen className="w-10 h-10 text-muted-foreground mx-auto" />
            <p className="text-sm text-muted-foreground">No projects yet. Create your first project.</p>
            <Button onClick={() => setDialogOpen(true)}><Plus className="w-4 h-4 mr-2" />Create Project</Button>
          </CardContent>
        ) : (
          <Table>
            <TableHeader>
              <TableRow><TableHead>Name</TableHead><TableHead>Language</TableHead><TableHead>Branch</TableHead><TableHead>Created</TableHead></TableRow>
            </TableHeader>
            <TableBody>
              {projects.map((p) => (
                <TableRow key={p.id}>
                  <TableCell>
                    <div className="font-medium">{p.name}</div>
                    {p.description && <div className="text-xs text-muted-foreground">{p.description}</div>}
                  </TableCell>
                  <TableCell><Badge variant="secondary">{p.language || "—"}</Badge></TableCell>
                  <TableCell><div className="flex items-center gap-1"><GitBranch className="w-3 h-3" /><span className="text-xs">{p.git_branch}</span></div></TableCell>
                  <TableCell className="text-xs text-muted-foreground">{p.created_at.slice(0, 10)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Card>
    </div>
  );
}
