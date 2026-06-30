"use client";
import { MotionConfig } from "framer-motion";

export function AnimationsProvider({ children }: { children: React.ReactNode }) {
  return (
    <MotionConfig reducedMotion="user">
      {children}
    </MotionConfig>
  );
}
