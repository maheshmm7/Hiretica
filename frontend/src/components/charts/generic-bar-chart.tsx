"use client";

import React, { useEffect, useState } from "react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function GenericBarChart({ data, color }: { data: any[], color: string }) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [Recharts, setRecharts] = useState<any>(null);

  useEffect(() => {
    import("recharts").then(mod => setRecharts(mod));
  }, []);

  if (!Recharts) {
    return <div className="w-full h-full flex items-center justify-center animate-pulse bg-muted/10 rounded-lg border border-border/50 text-sm text-muted-foreground">Loading chart...</div>;
  }

  const { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } = Recharts;
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
        <XAxis dataKey="name" stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
        <Tooltip 
          cursor={{fill: 'rgba(255,255,255,0.05)'}}
          contentStyle={{backgroundColor: '#111', borderColor: '#333', borderRadius: '8px'}}
        />
        <Bar dataKey="count" fill={color} radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
