"use client";

import React from "react";
import { PageHeader, SectionTitle } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { activeJob } from "@/lib/mock/jobs";
import { Badge } from "@/components/ui/badge";
import { Briefcase, MapPin, Clock, Building, Sparkles } from "lucide-react";
import { AIStatus } from "@/components/shared/status";

export default function JobUnderstandingPage() {
  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <PageHeader 
          title="Job Understanding" 
          description="AI parsed requirements from the active job description."
        />
        <AIStatus status="complete" className="mb-8 bg-background/50 border border-emerald-500/20 px-3 py-1.5 rounded-full" />
      </div>

      <AnimatedContainer delay={0.1}>
        <GlassPanel className="p-8">
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 mb-8 pb-8 border-b border-border/50">
            <div>
              <div className="flex items-center gap-3 mb-3">
                <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                  <Briefcase className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{activeJob.title}</h2>
                  <p className="text-muted-foreground">{activeJob.department} Department</p>
                </div>
              </div>
              
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mt-4">
                <div className="flex items-center gap-1.5"><MapPin className="h-4 w-4" /> {activeJob.location}</div>
                <div className="flex items-center gap-1.5"><Clock className="h-4 w-4" /> {activeJob.type}</div>
                <div className="flex items-center gap-1.5"><Building className="h-4 w-4" /> {activeJob.experience}</div>
              </div>
            </div>
            
            <Badge variant="outline" className="bg-primary/5 text-primary border-primary/20 hover:bg-primary/10 transition-colors">
              Active Requisition
            </Badge>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            <div className="lg:col-span-2 space-y-8">
              <div>
                <SectionTitle title="Description" />
                <p className="text-muted-foreground leading-relaxed">{activeJob.description}</p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Sparkles className="h-5 w-5 text-emerald-500" />
                  <h3 className="text-lg font-semibold">AI Extracted Core Skills</h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {activeJob.skills.map(skill => (
                    <Badge key={skill} variant="secondary" className="px-3 py-1 bg-secondary hover:bg-secondary/80">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-8">
              <div className="bg-muted/30 rounded-xl p-6 border border-border/50">
                <h3 className="font-semibold mb-4 flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-blue-500" /> Nice to Have
                </h3>
                <ul className="space-y-3">
                  {activeJob.niceToHave.map((item, i) => (
                    <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                      <span className="text-blue-500 mt-0.5">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-muted/30 rounded-xl p-6 border border-border/50">
                <h3 className="font-semibold mb-4">Metadata</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">ID</span>
                    <span className="font-medium">{activeJob.id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Posted</span>
                    <span className="font-medium">{new Date(activeJob.postedAt).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </GlassPanel>
      </AnimatedContainer>
    </div>
  );
}
