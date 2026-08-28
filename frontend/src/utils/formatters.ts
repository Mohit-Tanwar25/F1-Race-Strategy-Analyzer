export const getCompoundColor = (compound: string): string => {
  switch (compound.toUpperCase()) {
    case 'SOFT':
      return '#FF1801';
    case 'MEDIUM':
      return '#FFD800';
    case 'HARD':
      return '#FFFFFF';
    case 'INTERMEDIATE':
    case 'INTER':
      return '#39B54A';
    case 'WET':
      return '#00A3E0';
    default:
      return '#9CA3AF';
  }
};

export const getCompoundTextColor = (compound: string): string => {
  switch (compound.toUpperCase()) {
    case 'HARD':
    case 'MEDIUM':
      return '#10141E';
    default:
      return '#FFFFFF';
  }
};

export const formatLapTime = (seconds?: number | null): string => {
  if (seconds === undefined || seconds === null || isNaN(seconds) || seconds <= 0) {
    return '—';
  }
  const mins = Math.floor(seconds / 60);
  const remSecs = (seconds % 60).toFixed(3);
  return `${mins}:${remSecs.padStart(6, '0')}`;
};

export const formatDelta = (delta?: number | null): string => {
  if (delta === undefined || delta === null || isNaN(delta)) {
    return '—';
  }
  const sign = delta > 0 ? '+' : '';
  return `${sign}${delta.toFixed(3)}s`;
};
