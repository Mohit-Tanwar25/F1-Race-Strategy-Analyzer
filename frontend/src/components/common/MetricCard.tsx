import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subValue?: string;
  icon?: React.ReactNode;
  accentColor?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subValue,
  icon,
  accentColor,
}) => {
  return (
    <div className="telemetry-card p-4 flex flex-col justify-between relative overflow-hidden">
      {accentColor && (
        <div
          className="absolute top-0 left-0 right-0 h-1"
          style={{ backgroundColor: accentColor }}
        />
      )}
      <div className="flex items-center justify-between text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
        <span>{title}</span>
        {icon && <div className="text-slate-400">{icon}</div>}
      </div>
      <div className="text-2xl font-black font-mono tracking-tight text-white mt-1">
        {value}
      </div>
      {subValue && (
        <div className="text-xs text-slate-400 mt-1 flex items-center gap-1 font-medium">
          {subValue}
        </div>
      )}
    </div>
  );
};
