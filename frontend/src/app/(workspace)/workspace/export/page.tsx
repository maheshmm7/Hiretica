"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { AIStatus } from "@/components/shared/status";
import { Download, FileWarning, ArrowRight, FileText } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function ExportPage() {
  const workspace = useAppStore(state => state.workspace);

  if (!workspace) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-6 text-center">
        <FileWarning className="w-16 h-16 text-muted-foreground opacity-50" />
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">No Active Workspace</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            You need to select a job description and run the ranking pipeline before generating a submission export.
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

  const handleExport = () => {
    // Generate CSV from submission_preview
    const headers = ["candidate_id", "rank", "score", "reasoning"];
    const rows = workspace.submission_preview.map(c => 
      [c.candidate_id, c.rank, c.score, `"${c.reasoning.replace(/"/g, '""')}"`].join(",")
    );
    const csvContent = [headers.join(","), ...rows].join("\n");
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "submission.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Export Submission" 
          description="Generate the final CSV artifact required for the hackathon submission."
        />
        <AIStatus status="complete" className="mb-8 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <GlassPanel className="p-8 flex flex-col items-center justify-center text-center space-y-6 max-w-2xl mx-auto">
          <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center text-primary">
            <FileText className="w-10 h-10" />
          </div>
          
          <div className="space-y-2">
            <h2 className="text-2xl font-bold">Ready for Export</h2>
            <p className="text-muted-foreground">
              The AI pipeline has ranked {workspace.dashboard_metrics.total_candidates} candidates.
              The final payload matches the exact hackathon schema.
            </p>
          </div>
          
          <div className="bg-muted/50 p-4 rounded-lg border border-border w-full text-left text-sm font-mono text-muted-foreground">
            candidate_id,rank,score,reasoning<br/>
            {workspace.submission_preview[0].candidate_id},1,{workspace.submission_preview[0].score},&quot;...&quot;
          </div>

          <Button size="lg" className="w-full gap-2" onClick={handleExport}>
            <Download className="w-5 h-5" /> Download submission.csv
          </Button>
        </GlassPanel>
      </AnimatedContainer>
    </div>
  );
}
