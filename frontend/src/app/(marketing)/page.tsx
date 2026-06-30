"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, BrainCircuit, Database, Activity, Zap } from "lucide-react";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-primary/20 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-blue-500/10 blur-[120px] pointer-events-none" />

      {/* Header */}
      <header className="absolute top-0 w-full z-50 px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-primary text-primary-foreground flex items-center justify-center font-bold">
            H
          </div>
          <span className="font-bold text-xl tracking-tight">HIRETICA</span>
        </div>
        <Link href="/workspace/job-understanding">
          <Button variant="secondary" className="gap-2 font-medium bg-background/50 backdrop-blur-sm border border-border/50">
            Workspace <ArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 text-center pt-20">
        <AnimatedContainer delay={0.1} className="max-w-4xl mx-auto space-y-8">
          <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-4">
            <Zap className="mr-2 h-3.5 w-3.5" />
            Recruiter-Grade Candidate Intelligence
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground leading-[1.1]">
            Find the perfect candidate <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-500">
              with Explainable AI
            </span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Hiretica fuses Contextual AI, Precise Keyword Scoring, and Redrob Behavioral Signals to rank candidates exactly how a senior technical recruiter would.
          </p>

          <div className="flex items-center justify-center gap-4 pt-4">
            <Link href="/workspace/job-understanding">
              <Button size="lg" className="h-12 px-8 text-base font-medium rounded-full shadow-lg shadow-primary/25">
                Launch Workspace <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </Link>
          </div>
        </AnimatedContainer>

        {/* Feature Grid */}
        <AnimatedContainer delay={0.3} className="w-full max-w-6xl mt-24 grid grid-cols-1 md:grid-cols-3 gap-6 text-left pb-24">
          <GlassPanel className="p-8">
            <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-6 text-primary">
              <Database className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Hybrid Retrieval</h3>
            <p className="text-muted-foreground leading-relaxed">
              Combining deep contextual understanding with exact keyword matching to guarantee skill matching alongside contextual meaning.
            </p>
          </GlassPanel>

          <GlassPanel className="p-8">
            <div className="h-12 w-12 rounded-lg bg-blue-500/10 flex items-center justify-center mb-6 text-blue-500">
              <Activity className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Behavior Intelligence</h3>
            <p className="text-muted-foreground leading-relaxed">
              Analyzing candidate platform activity, response rates, and GitHub commits to predict true hiring intent.
            </p>
          </GlassPanel>

          <GlassPanel className="p-8">
            <div className="h-12 w-12 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-6 text-emerald-500">
              <BrainCircuit className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold mb-3">Explainable AI</h3>
            <p className="text-muted-foreground leading-relaxed">
              Generating transparent, human-readable rationales for why every candidate was ranked, enforcing recruiter trust.
            </p>
          </GlassPanel>
        </AnimatedContainer>
      </main>
    </div>
  );
}
