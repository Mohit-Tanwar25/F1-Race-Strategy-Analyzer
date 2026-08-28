import { describe, it, expect } from 'vitest';
import { getCompoundColor, formatLapTime, formatDelta } from '../utils/formatters';

describe('Formatters and Compound Utilities', () => {
  it('returns correct compound colors', () => {
    expect(getCompoundColor('SOFT')).toBe('#FF1801');
    expect(getCompoundColor('MEDIUM')).toBe('#FFD800');
    expect(getCompoundColor('HARD')).toBe('#FFFFFF');
    expect(getCompoundColor('INTERMEDIATE')).toBe('#39B54A');
    expect(getCompoundColor('WET')).toBe('#00A3E0');
    expect(getCompoundColor('UNKNOWN')).toBe('#9CA3AF');
  });

  it('formats lap times into M:SS.mmm format', () => {
    expect(formatLapTime(78.423)).toBe('1:18.423');
    expect(formatLapTime(90.05)).toBe('1:30.050');
    expect(formatLapTime(null)).toBe('—');
    expect(formatLapTime(undefined)).toBe('—');
    expect(formatLapTime(-5)).toBe('—');
  });

  it('formats delta times with sign', () => {
    expect(formatDelta(1.234)).toBe('+1.234s');
    expect(formatDelta(-0.567)).toBe('-0.567s');
    expect(formatDelta(null)).toBe('—');
  });
});
