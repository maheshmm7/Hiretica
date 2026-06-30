import { 
  Activity, Search, Users, Database, BrainCircuit, 
  Lightbulb, ShieldCheck, FileCheck, Download, Beaker, Settings
} from "lucide-react";

export const NAV_ITEMS = [
  { name: "Mission Control", href: "/workspace/mission-control", icon: Activity },
  { name: "Job Understanding", href: "/workspace/job-understanding", icon: Search },
  { name: "Candidate Intelligence", href: "/workspace/candidate-intelligence", icon: Users },
  { name: "Hybrid Retrieval", href: "/workspace/hybrid-retrieval", icon: Database },
  { name: "Recruiter Intelligence", href: "/workspace/recruiter-intelligence", icon: BrainCircuit },
  { name: "Behavior Intelligence", href: "/workspace/behavior-intelligence", icon: Lightbulb },
  { name: "Explainability", href: "/workspace/explainability", icon: ShieldCheck },
  { name: "Final Shortlist", href: "/workspace/final-shortlist", icon: FileCheck },
  { name: "Export", href: "/workspace/export", icon: Download },
  { name: "Science", href: "/workspace/science", icon: Beaker },
  { name: "Settings", href: "/workspace/settings", icon: Settings },
];
