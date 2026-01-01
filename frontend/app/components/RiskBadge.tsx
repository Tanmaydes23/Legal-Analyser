'use client';

import { Shield, AlertTriangle, CheckCircle, Info } from 'lucide-react';

interface RiskBadgeProps {
    level: 'Critical' | 'High' | 'Medium' | 'Low';
    score?: number;
    size?: 'sm' | 'md' | 'lg';
}

export default function RiskBadge({ level, score, size = 'md' }: RiskBadgeProps) {
    const configs = {
        Critical: {
            bg: 'bg-red-100',
            text: 'text-red-800',
            border: 'border-red-300',
            icon: AlertTriangle,
            emoji: '⛔'
        },
        High: {
            bg: 'bg-orange-100',
            text: 'text-orange-800',
            border: 'border-orange-300',
            icon: AlertTriangle,
            emoji: '⚠️'
        },
        Medium: {
            bg: 'bg-yellow-100',
            text: 'text-yellow-800',
            border: 'border-yellow-300',
            icon: Info,
            emoji: '⚡'
        },
        Low: {
            bg: 'bg-green-100',
            text: 'text-green-800',
            border: 'border-green-300',
            icon: CheckCircle,
            emoji: '✅'
        }
    };

    const config = configs[level];
    const Icon = config.icon;

    const sizes = {
        sm: 'px-2 py-1 text-xs',
        md: 'px-3 py-1.5 text-sm',
        lg: 'px-4 py-2 text-base'
    };

    return (
        <div className={`inline-flex items-center space-x-1.5 ${config.bg} ${config.text} ${config.border} border rounded-lg ${sizes[size]} font-semibold`}>
            <span>{config.emoji}</span>
            <span>{level} Risk</span>
            {score !== undefined && <span>({score.toFixed(0)}/100)</span>}
        </div>
    );
}