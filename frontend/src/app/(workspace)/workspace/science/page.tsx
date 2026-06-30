"use client";

import React from "react";
import { PageHeader, SectionTitle } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import {  Search, Database, BrainCircuit, Lightbulb, ShieldCheck } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function SciencePage() {
  return (
    <div className="space-y-8 pb-12">
      <PageHeader 
        title="Science & Architecture" 
        description="Deep dive into the algorithmic foundation and scoring logic powering HIRETICA."
      />

      <AnimatedContainer delay={0.1} className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassPanel className="p-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded bg-blue-500/10 text-blue-500">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold">Dense Vector Space</h3>
          </div>
          <Badge variant="outline" className="mb-4">sentence-transformers/all-MiniLM-L6-v2</Badge>
          <p className="text-muted-foreground leading-relaxed text-sm">
            We compute a 384-dimensional dense representation of a candidate&apos;s semantic career profile. This allows HIRETICA to understand that a &quot;Frontend Developer with React&quot; is semantically identical to a &quot;UI Engineer with Next.js&quot;, entirely bypassing the brittle nature of traditional keyword matching.
          </p>
          <div className="mt-4 p-4 rounded-lg bg-background/50 border border-border/50 text-xs font-mono text-muted-foreground">
            L2 Normalized inner product bounds: [-1, 1]
          </div>
        </GlassPanel>

        <GlassPanel className="p-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 rounded bg-amber-500/10 text-amber-500">
              <Search className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold">Keyword Matching Engine</h3>
          </div>
          <Badge variant="outline" className="mb-4 text-amber-500 border-amber-500/20">Exact Match Algorithm</Badge>
          <p className="text-muted-foreground leading-relaxed text-sm">
            Contextual AI sometimes misses specific technical acronyms (e.g. &quot;AWS&quot;, &quot;gRPC&quot;). We run a parallel keyword index specifically focused on extracting and hashing hard technical skills and certifications, guaranteeing exact-match resolution.
          </p>
          <div className="mt-4 p-4 rounded-lg bg-background/50 border border-border/50 text-xs font-mono text-muted-foreground">
            Term Frequency-Inverse Document Frequency (TF-IDF) evolution
          </div>
        </GlassPanel>
      </AnimatedContainer>

      <AnimatedContainer delay={0.2} className="space-y-6">
        <SectionTitle title="The Logic Engines" description="Applying recruiter intuition to mathematical probability." />
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <GlassPanel className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <BrainCircuit className="w-5 h-5 text-purple-500" />
              <h4 className="font-bold">Recruiter Intelligence</h4>
            </div>
            <p className="text-sm text-muted-foreground">
              Applies hard filtering rules simulating a human recruiter. For example, penalizing candidates whose location doesn&apos;t match the requisition, or boosting candidates with continuous tenure over job-hoppers.
            </p>
          </GlassPanel>

          <GlassPanel className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb className="w-5 h-5 text-rose-500" />
              <h4 className="font-bold">Behavior Intelligence</h4>
            </div>
            <p className="text-sm text-muted-foreground">
              Analyzes the simulated `redrob_signals`—metrics like `recruiter_response_rate`, `offer_acceptance_rate`, and `last_active_date`—to predict not just if a candidate is capable, but if they are likely to convert.
            </p>
          </GlassPanel>

          <GlassPanel className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <ShieldCheck className="w-5 h-5 text-emerald-500" />
              <h4 className="font-bold">Explainability Layer</h4>
            </div>
            <p className="text-sm text-muted-foreground">
              Every score modifier is tracked with a deterministic rationale (e.g. &quot;+5% (Tenure &gt; 4 years)&quot;). This prevents the &quot;black box&quot; AI problem, allowing recruiters to justify every ranking decision.
            </p>
          </GlassPanel>
        </div>
      </AnimatedContainer>
    </div>
  );
}
