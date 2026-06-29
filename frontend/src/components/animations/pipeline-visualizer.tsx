"use client";

import React from "react";
import { motion } from "framer-motion";
import { mockPipelineNodes } from "@/lib/mock/pipeline";
import { cn } from "@/lib/utils";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";
import { GlassPanel } from "../shared/containers";

export function PipelineVisualizer() {
  return (
    <GlassPanel className="p-8">
      <div className="flex flex-col md:flex-row items-center justify-between mb-8">
        <div>
          <h3 className="text-xl font-semibold">AI Execution Pipeline</h3>
          <p className="text-sm text-muted-foreground mt-1">Live status of the scoring engine</p>
        </div>
        <div className="flex items-center gap-4 text-sm mt-4 md:mt-0">
          <div className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-emerald-500" /> Complete</div>
          <div className="flex items-center gap-1.5"><Loader2 className="w-4 h-4 text-blue-500 animate-spin" /> Processing</div>
          <div className="flex items-center gap-1.5"><Circle className="w-4 h-4 text-muted-foreground" /> Pending</div>
        </div>
      </div>

      <div className="relative">
        {/* Connecting Line */}
        <div className="absolute left-[27px] top-4 bottom-4 w-0.5 bg-border z-0" />
        
        <div className="space-y-6 relative z-10">
          {mockPipelineNodes.map((node, i) => {
            const isComplete = node.status === "complete";
            const isProcessing = node.status === "processing";
            const isPending = node.status === "pending";

            return (
              <motion.div 
                key={node.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                className={cn(
                  "flex items-start gap-6 p-4 rounded-xl border transition-colors",
                  isComplete ? "bg-background/80 border-border" : 
                  isProcessing ? "bg-blue-500/5 border-blue-500/30 shadow-[0_0_15px_rgba(59,130,246,0.1)]" : 
                  "bg-muted/30 border-transparent opacity-60"
                )}
              >
                <div className={cn(
                  "flex-shrink-0 w-14 h-14 rounded-full border-4 border-background flex items-center justify-center bg-background shadow-sm",
                  isComplete ? "text-emerald-500" : isProcessing ? "text-blue-500" : "text-muted-foreground"
                )}>
                  {isComplete && <CheckCircle2 className="w-6 h-6" />}
                  {isProcessing && <Loader2 className="w-6 h-6 animate-spin" />}
                  {isPending && <span className="text-lg font-bold">{i + 1}</span>}
                </div>
                
                <div className="pt-1.5">
                  <h4 className={cn("text-base font-semibold", isProcessing && "text-blue-500 dark:text-blue-400")}>
                    {node.label}
                  </h4>
                  <p className="text-sm text-muted-foreground mt-1">{node.description}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </GlassPanel>
  );
}
