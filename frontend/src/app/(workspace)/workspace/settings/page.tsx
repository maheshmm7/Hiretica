"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { GlassPanel, AnimatedContainer } from "@/components/shared/containers";
import { useTheme } from "next-themes";
import { useQuery } from "@tanstack/react-query";
import { getHealth } from "@/lib/api/health";
import { getMetrics } from "@/lib/api/metrics";
import { Button } from "@/components/ui/button";
import { Server, Sun, Moon, Laptop, Database, Activity, CheckCircle2, XCircle, AlertTriangle, Trash2, FilePlus2, Settings as SettingsIcon } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { useAppStore } from "@/lib/store";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";

const subscribe = () => () => {};
const getSnapshot = () => "client";
const getServerSnapshot = () => "server";
export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const env = React.useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  const mounted = env === "client";

  const router = useRouter();
  const queryClient = useQueryClient();
  const resetWorkspace = useAppStore(state => state.resetWorkspace);
  const clearHistory = useAppStore(state => state.clearHistory);
  const factoryReset = useAppStore(state => state.factoryReset);

  const handleStartNewSession = () => {
    resetWorkspace();
    toast.success("New hiring session started successfully.");
    router.push("/workspace/job-understanding");
  };

  const handleClearHistory = () => {
    clearHistory();
    toast.success("Job history cleared successfully.");
  };

  const handleFactoryReset = () => {
    factoryReset();
    queryClient.clear();
    toast.success("Application reset successfully.");
    router.push("/workspace/job-understanding");
  };

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
    refetchInterval: 10000,
  });

  const { data: metrics } = useQuery({
    queryKey: ['metrics'],
    queryFn: getMetrics,
    refetchInterval: 10000,
  });

  return (
    <div className="space-y-8">
      <PageHeader 
        title="Settings" 
        description="Manage application preferences and monitor system health."
      />

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Appearance Settings */}
        <div className="space-y-6">
          <GlassPanel className="p-6">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Sun className="w-5 h-5 text-primary" /> Appearance
            </h3>
            <p className="text-sm text-muted-foreground mb-6">
              Customize the look and feel of the HIRETICA dashboard.
            </p>
            
            <div className="grid grid-cols-3 gap-4">
              <Button 
                variant={mounted && theme === "light" ? "default" : "outline"}
                className="flex flex-col items-center gap-2 h-auto py-4"
                onClick={() => setTheme("light")}
              >
                <Sun className="w-5 h-5" />
                <span>Light</span>
              </Button>
              <Button 
                variant={mounted && theme === "dark" ? "default" : "outline"}
                className="flex flex-col items-center gap-2 h-auto py-4"
                onClick={() => setTheme("dark")}
              >
                <Moon className="w-5 h-5" />
                <span>Dark</span>
              </Button>
              <Button 
                variant={mounted && theme === "system" ? "default" : "outline"}
                className="flex flex-col items-center gap-2 h-auto py-4"
                onClick={() => setTheme("system")}
              >
                <Laptop className="w-5 h-5" />
                <span>System</span>
              </Button>
            </div>
          </GlassPanel>

          {/* System Info */}
          <GlassPanel className="p-6">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" /> System Information
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Version</span>
                <span className="font-medium">{health?.version || "Loading..."}</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Environment</span>
                <span className="font-medium uppercase">Production</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Startup Time</span>
                <span className="font-medium">{metrics ? `${Math.round(metrics.startup_time_ms)}ms` : "Loading..."}</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Total Processed Candidates</span>
                <span className="font-medium">{metrics?.total_candidates_processed || 0}</span>
              </div>
            </div>
          </GlassPanel>
        </div>

        {/* API Status */}
        <div className="space-y-6">
          <GlassPanel className="p-6 h-full">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Server className="w-5 h-5 text-primary" /> API Health Status
            </h3>
            <p className="text-sm text-muted-foreground mb-6">
              Real-time monitoring of backend services and indices.
            </p>

            <div className="space-y-6">
              <div className="p-4 rounded-lg bg-background/50 border border-border/50">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 font-medium">
                    <Database className="w-4 h-4 text-blue-500" /> Contextual Vector Engine
                  </div>
                  {health?.components.faiss === 'ready' ? (
                    <Badge variant="outline" className="text-emerald-500 border-emerald-500/20 bg-emerald-500/10">
                      <CheckCircle2 className="w-3 h-3 mr-1" /> Online
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="text-red-500 border-red-500/20 bg-red-500/10">
                      <XCircle className="w-3 h-3 mr-1" /> Offline
                    </Badge>
                  )}
                </div>
                <Progress value={health?.components.faiss === 'ready' ? 100 : 0} className="h-1.5" />
              </div>

              <div className="p-4 rounded-lg bg-background/50 border border-border/50">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 font-medium">
                    <Database className="w-4 h-4 text-amber-500" /> Keyword Search Engine
                  </div>
                  {health?.components.bm25 === 'ready' ? (
                    <Badge variant="outline" className="text-emerald-500 border-emerald-500/20 bg-emerald-500/10">
                      <CheckCircle2 className="w-3 h-3 mr-1" /> Online
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="text-red-500 border-red-500/20 bg-red-500/10">
                      <XCircle className="w-3 h-3 mr-1" /> Offline
                    </Badge>
                  )}
                </div>
                <Progress value={health?.components.bm25 === 'ready' ? 100 : 0} className="h-1.5" />
              </div>

              <div className="p-4 rounded-lg bg-background/50 border border-border/50">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 font-medium">
                    <Activity className="w-4 h-4 text-purple-500" /> AI Pipeline Ensembles
                  </div>
                  {health?.components.pipeline === 'ready' ? (
                    <Badge variant="outline" className="text-emerald-500 border-emerald-500/20 bg-emerald-500/10">
                      <CheckCircle2 className="w-3 h-3 mr-1" /> Online
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="text-red-500 border-red-500/20 bg-red-500/10">
                      <XCircle className="w-3 h-3 mr-1" /> Offline
                    </Badge>
                  )}
                </div>
                <Progress value={health?.components.pipeline === 'ready' ? 100 : 0} className="h-1.5" />
              </div>
            </div>
          </GlassPanel>
        </div>

        {/* Workspace Management */}
        <div className="grid grid-cols-1 gap-6 max-w-5xl mt-6">
          <GlassPanel className="p-6">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <SettingsIcon className="w-5 h-5 text-primary" /> Workspace Management
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Action 1: Start New Hiring Session */}
              <div className="p-4 rounded-lg bg-background/50 border border-border/50 flex flex-col h-full">
                <div className="flex items-center gap-2 font-medium mb-2 text-primary">
                  <FilePlus2 className="w-5 h-5" /> Start New Session
                </div>
                <p className="text-sm text-muted-foreground mb-4 flex-1">
                  Start analyzing a completely new Job Description. This clears the current workspace but keeps your saved history.
                </p>
                <Button onClick={handleStartNewSession} className="w-full">
                  Start New Session
                </Button>
              </div>

              {/* Action 2: Clear Saved Job History */}
              <div className="p-4 rounded-lg bg-background/50 border border-border/50 flex flex-col h-full">
                <div className="flex items-center gap-2 font-medium mb-2 text-amber-500">
                  <Trash2 className="w-5 h-5" /> Clear History
                </div>
                <p className="text-sm text-muted-foreground mb-4 flex-1">
                  Permanently remove every saved Job Description from your local history.
                </p>
                <Dialog>
                  <DialogTrigger className="w-full inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 border bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2 text-amber-500 hover:text-amber-600 hover:bg-amber-500/10 border-amber-500/20">
                    Clear History
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Clear Job History</DialogTitle>
                      <DialogDescription>
                        This will permanently remove every saved Job Description. This action cannot be undone.
                      </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                      <DialogTrigger className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2">
                        Cancel
                      </DialogTrigger>
                      <DialogTrigger className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90 h-9 px-4 py-2" onClick={handleClearHistory}>
                        Clear History
                      </DialogTrigger>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>

              {/* Action 3: Factory Reset Application */}
              <div className="p-4 rounded-lg bg-red-500/5 border border-red-500/20 flex flex-col h-full">
                <div className="flex items-center gap-2 font-medium mb-2 text-red-500">
                  <AlertTriangle className="w-5 h-5" /> Factory Reset
                </div>
                <p className="text-sm text-muted-foreground mb-4 flex-1">
                  Permanently remove all data, cache, history, and workspace settings. Returns the application to first-launch state.
                </p>
                <Dialog>
                  <DialogTrigger className="w-full inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90 h-9 px-4 py-2">
                    Factory Reset
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Factory Reset Application</DialogTitle>
                      <DialogDescription>
                        <div className="space-y-4">
                          <p>This will permanently remove:</p>
                          <ul className="list-disc pl-4 space-y-1">
                            <li>Current workspace</li>
                            <li>Job history</li>
                            <li>Cached AI results</li>
                            <li>Selected candidates</li>
                            <li>Persisted Zustand storage</li>
                            <li>Local storage</li>
                            <li>Session storage</li>
                            <li>Notifications</li>
                            <li>Temporary application cache</li>
                          </ul>
                          <p className="font-bold text-red-500 mt-2">This action cannot be undone.</p>
                        </div>
                      </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                      <DialogTrigger className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2">
                        Cancel
                      </DialogTrigger>
                      <DialogTrigger className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90 h-9 px-4 py-2" onClick={handleFactoryReset}>
                        Factory Reset
                      </DialogTrigger>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
          </GlassPanel>
        </div>

      </AnimatedContainer>
    </div>
  );
}
