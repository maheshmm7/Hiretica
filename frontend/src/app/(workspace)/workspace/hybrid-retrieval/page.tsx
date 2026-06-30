"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { Database, Search, ArrowRight, FileWarning } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function HybridRetrievalPage() {
  const workspace = useAppStore(state => state.workspace);
  const selectedCandidate = useAppStore(state => state.selectedCandidate);
  const setSelectedCandidate = useAppStore(state => state.setSelectedCandidate);

  if (!workspace) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6 text-center">
        <FileWarning className="w-16 h-16 text-muted-foreground opacity-50" />
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">No Active Workspace</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            You need to select a job description and run the ranking pipeline before viewing retrieval results.
          </p>
        </div>
        <Link href="/workspace/job-understanding">
          <Button className="gap-2">
            Select Job Description <ArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </div>
    );
  }

  const candidates = workspace.candidates.toSorted((a, b) => b.hybrid_score - a.hybrid_score);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Candidate Retrieval" 
          description="Fusing Contextual Semantic Understanding and Precise Keyword Matching."
        />
        <AIStatus status="complete" className="mb-8 bg-blue-500/10 border border-blue-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassPanel className="p-6 border-blue-500/20">
          <div className="flex items-center gap-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-500">
              <Database className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-bold">Contextual Match (AI)</h3>
              <p className="text-xs text-muted-foreground">Understands the meaning beyond just keywords</p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="space-y-1.5">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Contextual understanding</span>
                <span className="font-medium text-blue-500">92%</span>
              </div>
              <Progress value={92} className="h-1.5 bg-blue-500/20" indicatorClassName="bg-blue-500" />
            </div>
            <p className="text-sm text-muted-foreground">
              Retrieves candidates who possess the underlying semantic concepts of the job description, bypassing keyword mismatches.
            </p>
          </div>
        </GlassPanel>

        <GlassPanel className="p-6 border-amber-500/20">
          <div className="flex items-center gap-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-500">
              <Search className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-bold">Keyword Match</h3>
              <p className="text-xs text-muted-foreground">Ensures critical required terms are present</p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="space-y-1.5">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Exact keyword intersection</span>
                <span className="font-medium text-amber-500">88%</span>
              </div>
              <Progress value={88} className="h-1.5 bg-amber-500/20" indicatorClassName="bg-amber-500" />
            </div>
            <p className="text-sm text-muted-foreground">
              Enforces strict occurrence of mandatory technical terms (e.g., &quot;Kubernetes&quot;, &quot;AWS&quot;) that semantic models might overly generalize.
            </p>
          </div>
        </GlassPanel>
      </AnimatedContainer>

      <AnimatedContainer delay={0.2}>
        <h3 className="text-lg font-bold mb-4">Initial Fusion Ranking (Top 100)</h3>
        <GlassPanel className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase text-muted-foreground bg-muted/50 border-b border-border">
                <tr>
                  <th className="px-6 py-4 font-medium">Candidate</th>
                  <th className="px-6 py-4 font-medium">Contextual Score</th>
                  <th className="px-6 py-4 font-medium">Keyword Score</th>
                  <th className="px-6 py-4 font-medium text-primary">Match Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/50">
                {candidates.slice(0, 100).map((candidate) => (
                  <tr 
                    key={candidate.candidate_id} 
                    className={`transition-colors cursor-pointer ${selectedCandidate === candidate.candidate_id ? 'bg-primary/10 border-l-2 border-primary' : 'hover:bg-muted/30'}`}
                    onClick={() => setSelectedCandidate(candidate.candidate_id)}
                  >
                    <td className="px-6 py-4">
                      <div className="font-medium text-foreground">{candidate.candidate_id}</div>
                      <div className="text-xs text-muted-foreground">Candidate Profile</div>
                    </td>
                    <td className="px-6 py-4 text-blue-500 font-medium">{candidate.faiss_score !== undefined ? (candidate.faiss_score * 100).toFixed(1) : '---'}</td>
                    <td className="px-6 py-4 text-amber-500 font-medium">{candidate.bm25_score !== undefined ? (candidate.bm25_score * 100).toFixed(1) : '---'}</td>
                    <td className="px-6 py-4 font-bold text-primary flex items-center gap-2">
                      {(candidate.hybrid_score * 100).toFixed(1)} <ArrowRight className="w-3 h-3 text-muted-foreground" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>
      </AnimatedContainer>
    </div>
  );
}
