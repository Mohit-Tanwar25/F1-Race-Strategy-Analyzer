import React from 'react';
import { getCompoundColor, getCompoundTextColor } from '../../utils/formatters';

interface CompoundBadgeProps {
  compound: string;
  tyreAge?: number;
  size?: 'sm' | 'md' | 'lg';
}

export const CompoundBadge: React.FC<CompoundBadgeProps> = ({
  compound,
  tyreAge,
  size = 'md',
}) => {
  const color = getCompoundColor(compound);
  const textColor = getCompoundTextColor(compound);

  const sizeClasses = {
    sm: 'px-1.5 py-0.5 text-[10px]',
    md: 'px-2.5 py-0.5 text-xs',
    lg: 'px-3 py-1 text-sm',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded font-bold tracking-wider uppercase font-mono shadow-sm ${sizeClasses[size]}`}
      style={{ backgroundColor: color, color: textColor }}
    >
      <span className="w-1.5 h-1.5 rounded-full border border-black/30 bg-current"></span>
      {compound}
      {tyreAge !== undefined && (
        <span className="opacity-80 font-normal">({tyreAge}L)</span>
      )}
    </span>
  );
};
