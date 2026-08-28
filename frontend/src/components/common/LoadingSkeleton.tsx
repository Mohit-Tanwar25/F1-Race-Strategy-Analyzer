import React from 'react';

export const LoadingSkeleton: React.FC<{ rows?: number; height?: string }> = ({
  rows = 4,
  height = 'h-10',
}) => {
  return (
    <div className="w-full space-y-3 animate-pulse">
      {Array.from({ length: rows }).map((_, i) => (
        <div
          key={i}
          className={`w-full bg-[#1F2739] rounded-lg ${height}`}
          style={{ opacity: 1 - i * 0.15 }}
        />
      ))}
    </div>
  );
};
