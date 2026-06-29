"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { Sun, Moon, Bell } from "lucide-react";
import { Breadcrumb, BreadcrumbItem, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbLink } from "@/components/ui/breadcrumb";

export function Topbar() {
  const { setTheme, theme } = useTheme();
  const pathname = usePathname();
  
  const segments = pathname.split('/').filter(Boolean);
  const currentSegment = segments[segments.length - 1] || '';
  const title = currentSegment.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' ');

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-30">
      <div className="flex items-center gap-4">
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem className="hidden sm:block">
              <BreadcrumbLink href="/workspace/mission-control">Workspace</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator className="hidden sm:block" />
            <BreadcrumbItem>
              <BreadcrumbPage className="font-medium text-foreground">{title || "Overview"}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" className="text-muted-foreground">
          <Bell className="w-4 h-4" />
        </Button>
        <Button 
          variant="ghost" 
          size="icon" 
          className="text-muted-foreground"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </div>
    </header>
  );
}
