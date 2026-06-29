"use client";

import React from "react";
import { PageHeader } from "@/components/shared/typography";
import { AnimatedContainer, GlassPanel } from "@/components/shared/containers";
import { mockCandidates } from "@/lib/mock/candidates";
import { Badge } from "@/components/ui/badge";
import { Search, MapPin, Briefcase } from "lucide-react";
import { Input } from "@/components/ui/input";

export default function CandidateIntelligencePage() {
  return (
    <div className="space-y-8">
      <PageHeader 
        title="Candidate Intelligence" 
        description="Explore the global candidate pool and extracted semantic features."
      />

      <AnimatedContainer delay={0.1}>
        <div className="relative mb-8 max-w-xl">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <Input 
            placeholder="Search by name, role, or skill..." 
            className="pl-10 h-12 bg-background/50 backdrop-blur-sm border-border/50 focus-visible:ring-primary/20"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {mockCandidates.map((candidate, i) => (
            <GlassPanel key={candidate.id} className="p-6 hover:border-primary/20 transition-colors cursor-pointer group">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold group-hover:text-primary transition-colors">{candidate.name}</h3>
                  <p className="text-sm font-medium text-foreground/80 mt-1">{candidate.headline}</p>
                </div>
                <div className="text-right">
                  <div className="text-xs text-muted-foreground mb-1">Match Score</div>
                  <div className="text-2xl font-bold text-emerald-500">{candidate.matchScore.toFixed(1)}</div>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground mb-6">
                <div className="flex items-center gap-1.5"><MapPin className="h-3.5 w-3.5" /> {candidate.location}</div>
                <div className="flex items-center gap-1.5"><Briefcase className="h-3.5 w-3.5" /> {candidate.experience}y exp</div>
                <div className="flex items-center gap-1.5"><Briefcase className="h-3.5 w-3.5" /> {candidate.currentCompany}</div>
              </div>

              <div className="space-y-3">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Top Skills</div>
                <div className="flex flex-wrap gap-2">
                  {candidate.skills.slice(0, 4).map(skill => (
                    <Badge 
                      key={skill.name} 
                      variant="secondary" 
                      className={skill.match ? "bg-primary/10 text-primary hover:bg-primary/20 border-primary/20" : "bg-muted text-muted-foreground"}
                    >
                      {skill.name}
                    </Badge>
                  ))}
                  {candidate.skills.length > 4 && (
                    <Badge variant="outline" className="text-muted-foreground">+{candidate.skills.length - 4} more</Badge>
                  )}
                </div>
              </div>
            </GlassPanel>
          ))}
        </div>
      </AnimatedContainer>
    </div>
  );
}
