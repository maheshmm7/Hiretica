"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { Badge } from "@/components/ui/badge";
import { Briefcase, Sparkles, Play, Loader2, FileText, CheckCircle2, AlertCircle, History, Trash2 } from "lucide-react";
import { AIStatus } from "@/components/shared/status";
import { Button } from "@/components/ui/button";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { analyzeJob } from "@/lib/api/ranking";
import { useAppStore, JobHistoryItem } from "@/lib/store";
import { useRouter } from "next/navigation";



const SAMPLES = [
  "We are looking for a Machine Learning Engineer with strong Python and PyTorch experience to join our core AI team. You should have 4+ years of experience building scalable systems and deploying models to production. Nice to have: Agile, Docker, Kubernetes.",
  "Seeking a Senior Frontend Developer with expertise in React, Next.js, and TailwindCSS. 5+ years of experience required. Must have a strong eye for design and experience with WebGL or Three.js is a plus.",
  "Data Scientist needed for our analytics team. Requirements: SQL, Python, Pandas, Scikit-learn, and 3+ years of experience. A background in finance or economics is highly preferred.",
  "Product Manager with 6+ years of experience. Must have experience leading cross-functional teams and launching B2B SaaS products. Excellent communication skills required."
];

export default function JobUnderstandingPage() {
  const router = useRouter();
  
  const jobDescription = useAppStore(state => state.jobDescription);
  const setJobDescription = useAppStore(state => state.setJobDescription);
  
  const analysis = useAppStore(state => state.parsedUnderstanding);
  const setAnalysis = useAppStore(state => state.setParsedUnderstanding);
  
  const setPipelineStatus = useAppStore(state => state.setPipelineStatus);
  const clearWorkspace = useAppStore(state => state.clearWorkspace);
  const history = useAppStore(state => state.history);
  const saveToHistory = useAppStore(state => state.saveToHistory);
  const deleteHistoryItem = useAppStore(state => state.deleteHistoryItem);

  const queryClient = useQueryClient();


  const loadHistoryItem = (item: JobHistoryItem) => {
    setJobDescription(item.text);
    setAnalysis(item.parsed);
  };

  const analyzeMutation = useMutation({
    mutationFn: () => analyzeJob("REQ-100", jobDescription),
    onSuccess: (data) => {
      setAnalysis(data);
      saveToHistory(jobDescription, data);
      queryClient.invalidateQueries();
    }
  });

  const handleRank = () => {
    clearWorkspace();
    setPipelineStatus('processing');
    router.push("/workspace/mission-control");
  };


  const loadSample = () => {
    const currentIdx = SAMPLES.indexOf(jobDescription);
    const nextIdx = (currentIdx + 1) % SAMPLES.length;
    setJobDescription(SAMPLES[nextIdx]);
    setAnalysis(null);
  };

  return (
    <div className="flex flex-col md:flex-row gap-8">
      <div className="flex-1 space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <PageHeader 
            title="Job Understanding" 
            description="Provide a job description for the AI to analyze before ranking candidates."
          />
          <div className="flex items-center gap-4">
            <div className={`transition-opacity duration-300 ${analysis && !analysis.validation_warning ? 'opacity-100' : 'opacity-0'}`}>
              <AIStatus status="complete" className="bg-background/50 border border-emerald-500/20 px-3 py-1.5 rounded-full" />
            </div>
            
            <Button 
              onClick={() => analyzeMutation.mutate()} 
              disabled={analyzeMutation.isPending || jobDescription.length < 10}
              variant={analysis && !analysis.validation_warning ? "outline" : "default"}
              className="gap-2"
            >
              {analyzeMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              {analyzeMutation.isPending ? "Analyzing..." : (analysis && !analysis.validation_warning ? "Re-Analyze" : "Analyze Job")}
            </Button>

            <Button 
              onClick={handleRank}
              disabled={!analysis || !!analysis.validation_warning}
              className={`gap-2 transition-all ${analysis && !analysis.validation_warning ? 'bg-emerald-600 hover:bg-emerald-700 text-white' : 'bg-muted text-muted-foreground'}`}
            >
              <Play className="w-4 h-4" />
              Rank Candidates
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <AnimatedContainer delay={0.1}>
            <GlassPanel className="p-6 h-full flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <FileText className="w-5 h-5 text-primary" />
                  Job Description
                </h3>
                <Button variant="ghost" size="sm" onClick={loadSample} className="text-xs">
                  Load Sample Job
                </Button>
              </div>
              <textarea
                aria-label="Job Description"
                className="flex-1 w-full min-h-[400px] rounded-lg border border-border/50 bg-background/50 p-4 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 resize-none"
                placeholder="Paste the job description here..."
                value={jobDescription}
                onChange={(e) => {
                  const val = e.target.value;
                  setJobDescription(val);
                  if (analysis && val !== jobDescription) {
                     setAnalysis(null);
                  }
                }}
                disabled={analyzeMutation.isPending}
              />
            </GlassPanel>
          </AnimatedContainer>

          <AnimatedContainer delay={0.2}>
            <GlassPanel className="p-6 h-full">
              <h3 className="text-lg font-semibold flex items-center gap-2 mb-6">
                <Sparkles className="w-5 h-5 text-emerald-500" />
                AI Understanding
              </h3>
              
              {analyzeMutation.isPending ? (
                <div className="flex flex-col items-center justify-center h-[400px] text-muted-foreground space-y-4">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                  <p>Analyzing requirements, skills, and experience...</p>
                </div>
              ) : analysis ? (
                analysis.validation_warning ? (
                  <div className="flex flex-col items-center justify-center h-[400px] text-destructive text-center px-8 border-2 border-dashed border-destructive/50 rounded-xl bg-destructive/10">
                    <AlertCircle className="w-8 h-8 mb-4" />
                    <p className="font-semibold mb-2">Invalid Job Description</p>
                    <p className="text-sm opacity-80">{analysis.validation_warning}</p>
                    <Button variant="outline" className="mt-4" onClick={() => setAnalysis(null)}>Try Again</Button>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div>
                      <div className="text-sm text-muted-foreground mb-1">Inferred Role</div>
                      <div className="text-xl font-semibold text-primary">{analysis.role}</div>
                    </div>

                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Summary</div>
                      <p className="text-sm leading-relaxed">{analysis.summary}</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-muted/30 p-4 rounded-lg border border-border/50">
                        <div className="text-sm text-muted-foreground mb-1 flex items-center gap-2">
                          <Briefcase className="w-4 h-4" /> Required Experience
                        </div>
                        <div className="font-medium">{analysis.required_experience}</div>
                      </div>
                      <div className="bg-muted/30 p-4 rounded-lg border border-border/50">
                        <div className="text-sm text-muted-foreground mb-1 flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Confidence
                        </div>
                        <div className="font-medium">{Math.round(analysis.confidence_score * 100)}%</div>
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Core Skills</div>
                      <div className="flex flex-wrap gap-2">
                        {analysis.core_skills.length > 0 ? analysis.core_skills.map((skill) => (
                          <Badge key={skill} variant="secondary" className="bg-primary/10 hover:bg-primary/20 text-primary border-primary/20">
                            {skill}
                          </Badge>
                        )) : <span className="text-sm text-muted-foreground">Not Specified</span>}
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-muted-foreground mb-2">Nice-to-have Skills</div>
                      <div className="flex flex-wrap gap-2">
                        {analysis.nice_to_have.length > 0 ? analysis.nice_to_have.map((skill) => (
                          <Badge key={skill} variant="outline" className="text-muted-foreground">
                            {skill}
                          </Badge>
                        )) : <span className="text-sm text-muted-foreground">Not Specified</span>}
                      </div>
                    </div>
                  </div>
                )
              ) : (
                <div className="flex flex-col items-center justify-center h-[400px] text-muted-foreground text-center px-8 border-2 border-dashed border-border/50 rounded-xl bg-muted/10">
                  <Sparkles className="w-8 h-8 mb-4 opacity-50" />
                  <p>Paste a job description and click &quot;Analyze Job&quot; to see what the AI understands about this role.</p>
                </div>
              )}
            </GlassPanel>
          </AnimatedContainer>
        </div>
      </div>
      
      {/* Sidebar for History */}
      <div className="w-full md:w-64 shrink-0">
        <GlassPanel className="p-4 h-full min-h-[500px]">
          <h3 className="text-sm font-semibold flex items-center gap-2 mb-4 text-muted-foreground uppercase tracking-wider">
            <History className="w-4 h-4" />
            Recent Jobs
          </h3>
          <div className="space-y-3">
            {history.length === 0 ? (
              <p className="text-xs text-muted-foreground text-center py-8">No recent jobs found.</p>
            ) : (
              history.map(item => (
                <div 
                  role="button"
                  tabIndex={0}
                  key={item.id} 
                  className="w-full text-left p-3 rounded-lg bg-background/50 border border-border/50 hover:border-primary/50 transition-colors group cursor-pointer block" 
                  onClick={() => loadHistoryItem(item)}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') loadHistoryItem(item); }}
                >
                  <div className="font-medium text-sm truncate">{item.title}</div>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-xs text-muted-foreground">{new Date(item.timestamp).toLocaleDateString()}</span>
                    <Button variant="ghost" size="icon" className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:bg-destructive/10" onClick={(e) => { e.stopPropagation(); deleteHistoryItem(item.id); }}>
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </GlassPanel>
      </div>
    </div>
  );
}
