"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { MetricCard } from "@/components/shared/metric-card";
import { AnimatedContainer } from "@/components/shared/containers";
import { PipelineVisualizer } from "@/components/animations/pipeline-visualizer";
import { mockMetrics } from "@/lib/mock/metrics";
import { Database, Server, Users, Zap, CheckCircle2, Clock } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

export default function MissionControlPage() {
  return (
    <div className="space-y-8">
      <PageHeader 
        title="Mission Control" 
        description="Real-time overview of the HIRETICA engine and pipeline status."
      />

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard 
          title="System Health" 
          value={`${mockMetrics.pipelineHealth}%`} 
          icon={Server} 
          trend={{ value: 0.5, label: "vs last hour", positive: true }} 
          className="border-emerald-500/20 shadow-[0_0_20px_rgba(16,185,129,0.05)]"
        />
        <MetricCard 
          title="Candidate Profiles" 
          value={(mockMetrics.totalCandidates / 1000).toFixed(0) + "k"} 
          description="Total processed across pipeline"
          icon={Users} 
        />
        <MetricCard 
          title="Avg Processing Time" 
          value={`${mockMetrics.avgProcessingTimeMs}ms`} 
          description="Per query candidate matching"
          icon={Zap} 
        />
        <MetricCard 
          title="Shortlisted" 
          value={mockMetrics.shortlisted} 
          description="Candidates passing final threshold"
          icon={CheckCircle2} 
        />
      </AnimatedContainer>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <AnimatedContainer delay={0.2} className="lg:col-span-2">
          <PipelineVisualizer />
        </AnimatedContainer>

        <AnimatedContainer delay={0.3} className="space-y-8">
          <Card className="bg-background/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="text-lg">Index Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium flex items-center gap-2"><Database className="w-4 h-4 text-blue-500" /> FAISS Vector Index</span>
                  <span className="text-emerald-500 font-medium">Online</span>
                </div>
                <Progress value={100} className="h-2" />
                <p className="text-xs text-muted-foreground">100,000 dense embeddings mapped.</p>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium flex items-center gap-2"><Database className="w-4 h-4 text-amber-500" /> BM25 Lexical Index</span>
                  <span className="text-emerald-500 font-medium">Online</span>
                </div>
                <Progress value={100} className="h-2" />
                <p className="text-xs text-muted-foreground">Lexical tokens generated for fast exact-match.</p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium flex items-center gap-2"><Database className="w-4 h-4 text-purple-500" /> DuckDB Analytics</span>
                  <span className="text-amber-500 font-medium">Building</span>
                </div>
                <Progress value={45} className="h-2" />
                <p className="text-xs text-muted-foreground">Materializing parquet files into memory.</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-background/50 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="text-lg">Active Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <div className="flex justify-between py-2 border-b border-border/50">
                <span className="text-muted-foreground">Embedding Model</span>
                <span className="font-medium">all-MiniLM-L6-v2</span>
              </div>
              <div className="flex justify-between py-2 border-b border-border/50">
                <span className="text-muted-foreground">Vector Dimensions</span>
                <span className="font-medium">384</span>
              </div>
              <div className="flex justify-between py-2 border-b border-border/50">
                <span className="text-muted-foreground">Similarity Metric</span>
                <span className="font-medium">Inner Product (IP)</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-muted-foreground">Last Updated</span>
                <span className="font-medium flex items-center gap-1.5"><Clock className="w-3 h-3" /> Just now</span>
              </div>
            </CardContent>
          </Card>
        </AnimatedContainer>
      </div>
    </div>
  );
}
