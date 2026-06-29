"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { mockCandidates } from "@/lib/mock/candidates";
import { Database, Search, ArrowRight } from "lucide-react";
import { Progress } from "@/components/ui/progress";

export default function HybridRetrievalPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Hybrid Retrieval" 
          description="Fusing Dense Vector Search (FAISS) and Lexical Exact-Match (BM25)."
        />
        <AIStatus status="processing" className="mb-8 bg-blue-500/10 border border-blue-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassPanel className="p-6 border-blue-500/20">
          <div className="flex items-center gap-3 mb-6">
            <div className="h-10 w-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-500">
              <Database className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-bold">Dense Vector Retrieval</h3>
              <p className="text-xs text-muted-foreground">all-MiniLM-L6-v2 + FAISS IndexFlatIP</p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="space-y-1.5">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Semantic matching coverage</span>
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
              <h3 className="font-bold">Lexical Exact Match</h3>
              <p className="text-xs text-muted-foreground">BM25 Okapi Algorithm</p>
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
              Enforces strict occurrence of mandatory technical terms (e.g., "Kubernetes", "AWS") that semantic models might overly generalize.
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
                  <th className="px-6 py-4 font-medium">FAISS Score</th>
                  <th className="px-6 py-4 font-medium">BM25 Score</th>
                  <th className="px-6 py-4 font-medium text-primary">Hybrid Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/50">
                {mockCandidates.map((candidate) => (
                  <tr key={candidate.id} className="hover:bg-muted/30 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-medium text-foreground">{candidate.name}</div>
                      <div className="text-xs text-muted-foreground">{candidate.currentRole}</div>
                    </td>
                    <td className="px-6 py-4 text-blue-500 font-medium">0.892</td>
                    <td className="px-6 py-4 text-amber-500 font-medium">14.320</td>
                    <td className="px-6 py-4 font-bold text-primary flex items-center gap-2">
                      {candidate.hybridScore.toFixed(1)} <ArrowRight className="w-3 h-3 text-muted-foreground" />
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
