"use client";

import React, { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { PageHeader } from "@/components/shared/typography";
import { MetricCard } from "@/components/shared/metric-card";
import { AnimatedContainer } from "@/components/shared/containers";
import { PipelineVisualizer } from "@/components/animations/pipeline-visualizer";
import { getHealth } from "@/lib/api/health";
import { getMetrics } from "@/lib/api/metrics";
import { rankWorkspace } from "@/lib/api/ranking";
import { useAppStore } from "@/lib/store";
import { useRouter } from "next/navigation";
import { Database, Server, Users, Zap, CheckCircle2, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function MissionControlPage() {
  const router = useRouter();
  
  const workspace = useAppStore(state => state.workspace);
  const setWorkspace = useAppStore(state => state.setWorkspace);
  
  const queryClient = useQueryClient();
  const pipelineStatus = useAppStore(state => state.pipelineStatus);
  const setPipelineStatus = useAppStore(state => state.setPipelineStatus);
  
  const jobDescription = useAppStore(state => state.jobDescription);
  
  // Pipeline animation state
  const [currentStage, setCurrentStage] = useState<number>(-1);

  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
    refetchInterval: 10000,
  });

  const { data: metrics, isLoading: metricsLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: getMetrics,
    refetchInterval: 10000,
  });

  const rankMutation = useMutation({
    mutationFn: (jd: string) => rankWorkspace("REQ-100", jd),
    onSuccess: (data) => {
      setWorkspace(data);
      setPipelineStatus('completed');
      setCurrentStage(10); // complete
      queryClient.invalidateQueries();
      toast.success("Pipeline Execution Complete", {
        description: `Successfully ranked ${data.dashboard_metrics.total_candidates} candidates.`
      });
    },
    onError: () => {
      setPipelineStatus('idle');
      setCurrentStage(-1);
      toast.error("Pipeline Error", {
        description: "Failed to rank candidates. Please check backend logs."
      });
    }
  });

  useEffect(() => {
    if (pipelineStatus === 'completed' && workspace) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setCurrentStage(10);
    } else if (pipelineStatus === 'processing' && jobDescription && !rankMutation.isPending && !workspace) {
      setCurrentStage(0);
      rankMutation.mutate(jobDescription);
    } else if (pipelineStatus === 'processing' && workspace) {
      // shouldn't happen usually, but if it does, set to complete
      setPipelineStatus('completed');
      setCurrentStage(10);
    }
  }, [pipelineStatus, jobDescription, workspace, rankMutation, setPipelineStatus]);

  // Simulate pipeline stages visually while the mutation is pending
  useEffect(() => {
    if (currentStage >= 0 && currentStage < 9 && pipelineStatus === 'processing') {
      const timer = setTimeout(() => {
        setCurrentStage(prev => prev + 1);
      }, 1500); // 1.5 seconds per fake stage
      return () => clearTimeout(timer);
    }
  }, [currentStage, pipelineStatus]);

  if (healthLoading || metricsLoading) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }
  
  const isHealthy = health?.status === 'ok';

  if (!jobDescription) {
    return (
      <div className="space-y-8">
        <PageHeader 
          title="Mission Control" 
          description="Real-time overview of the HIRETICA engine and pipeline status."
        />
        <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-6">
          <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
            <Loader2 className="w-8 h-8 text-muted-foreground animate-spin" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-2">Waiting for Job Description</h2>
            <p className="text-muted-foreground max-w-md mx-auto">Please go to Job Understanding, analyze a job description, and click Rank Candidates to begin the pipeline.</p>
          </div>
          <Button onClick={() => router.push("/workspace/job-understanding")}>
            Go to Job Understanding
          </Button>
        </div>
      </div>
    );
  }

  const isFinished = pipelineStatus === 'completed' && workspace;
  const isProcessing = pipelineStatus === 'processing' || rankMutation.isPending;

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Mission Control" 
          description="Real-time overview of the HIRETICA engine and pipeline status."
        />
        {isFinished && (
          <div className="flex items-center gap-4">
            <div className="text-sm font-medium text-emerald-500 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5" /> Pipeline Complete ({workspace?.dashboard_metrics.total_candidates} Candidates Ranked)
            </div>
            <Button onClick={() => router.push("/workspace/candidate-intelligence")}>
              View Results
            </Button>
          </div>
        )}
      </div>

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard 
          title="System Health" 
          value={isHealthy ? "100%" : "Offline"} 
          icon={Server} 
          trend={{ value: 0, label: "vs last hour", positive: isHealthy }} 
          className={isHealthy ? "border-emerald-500/20 shadow-[0_0_20px_rgba(16,185,129,0.05)]" : "border-red-500/20 shadow-[0_0_20px_rgba(239,68,68,0.05)]"}
        />
        <MetricCard 
          title="Pipeline Status" 
          value={isFinished ? "Completed" : isProcessing ? "Running" : "Ready"} 
          description="Model weights & indices"
          icon={Users} 
        />
        <MetricCard 
          title="Startup Time" 
          value={metrics ? `${Math.round(metrics.startup_time_ms)}ms` : "---"} 
          description="Cold boot latency"
          icon={Zap} 
        />
        <MetricCard 
          title="Version" 
          value={health?.version || "---"} 
          description="Current deployment API version"
          icon={CheckCircle2} 
        />
      </AnimatedContainer>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <AnimatedContainer delay={0.2} className="lg:col-span-2">
          <PipelineVisualizer activeStage={currentStage} />
        </AnimatedContainer>

        <AnimatedContainer delay={0.3} className="space-y-8">
          <Card className="bg-background/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="text-lg">Index Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium flex items-center gap-2"><Database className="w-4 h-4 text-blue-500" /> Contextual Match Engine</span>
                  <span className={health?.components.faiss === 'ready' ? "text-emerald-500 font-medium" : "text-amber-500 font-medium"}>
                    {health?.components.faiss === 'ready' ? "Online" : "Offline"}
                  </span>
                </div>
                <Progress value={health?.components.faiss === 'ready' ? 100 : 0} className="h-2" />
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium flex items-center gap-2"><Database className="w-4 h-4 text-amber-500" /> Keyword Match Engine</span>
                  <span className={health?.components.bm25 === 'ready' ? "text-emerald-500 font-medium" : "text-amber-500 font-medium"}>
                     {health?.components.bm25 === 'ready' ? "Online" : "Offline"}
                  </span>
                </div>
                <Progress value={health?.components.bm25 === 'ready' ? 100 : 0} className="h-2" />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium flex items-center gap-2"><Database className="w-4 h-4 text-purple-500" /> AI Pipeline</span>
                  <span className={health?.components.pipeline === 'ready' ? "text-emerald-500 font-medium" : "text-amber-500 font-medium"}>
                    {health?.components.pipeline === 'ready' ? "Ready" : "Initializing"}
                  </span>
                </div>
                <Progress value={health?.components.pipeline === 'ready' ? 100 : 45} className="h-2" />
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>
    </div>
  );
}
