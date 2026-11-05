import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Coin, CORAL, Float, INK, Pop, PURPLE, SKY, Stage, Star, SUN, TEAL} from './Scenes';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const PANEL = {left: 60, right: 1020, top: 330, bottom: 910};

const Enter: React.FC<{children: React.ReactNode}> = ({children}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = spring({frame: f, fps, config: {damping: 15, stiffness: 130}});
	return <div style={{position: 'absolute', inset: 0, opacity: p, transform: `translateY(${(1 - p) * 40}px)`}}>{children}</div>;
};
const Title = ({t, icon}: {t: string; icon?: React.ReactNode}) => <div style={{position: 'absolute', left: 90, right: 140, top: 210, fontSize: 44, fontWeight: 700, color: INK, display: 'flex', alignItems: 'center', gap: 18}}>{icon}{t}</div>;
const Note = ({t}: {t: string}) => <div style={{position: 'absolute', left: 90, right: 140, top: 930, fontSize: 28, color: INK, background: 'rgba(255,255,255,.82)', padding: '4px 14px', borderRadius: 12}}>{t}</div>;

const path = (v: number[], lo: number, hi: number, progress = 1) => {
	const w = PANEL.right - PANEL.left - 80;
	const h = PANEL.bottom - PANEL.top - 90;
	const n = Math.max(2, Math.ceil(v.length * progress));
	return v.slice(0, n).map((y, i) => `${i ? 'L' : 'M'}${(PANEL.left + 40 + (i / (v.length - 1)) * w).toFixed(1)} ${(PANEL.top + 60 + (1 - (y - lo) / (hi - lo)) * h).toFixed(1)}`).join('');
};
const ChartFrame: React.FC<{children: React.ReactNode}> = ({children}) => (
	<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
		<rect x={PANEL.left} y={PANEL.top} width={PANEL.right - PANEL.left} height={PANEL.bottom - PANEL.top} rx={32} fill="#fff" stroke="#e7e2d0" strokeWidth={4} />
		{children}
	</svg>
);
const Legend = ({a, b, ca, cb}: {a: string; b: string; ca: string; cb: string}) => (
	<div style={{position: 'absolute', left: 100, top: 345, display: 'flex', gap: 34, fontSize: 36, fontWeight: 700}}>
		<span style={{color: ca}}>● {a}</span>
		<span style={{color: cb}}>● {b}</span>
	</div>
);
export const DualLine = ({a, b, labelA, labelB, title, note, icon, colorB = CORAL}: {a: number[]; b: number[]; labelA: string; labelB: string; title: string; note: string; icon?: React.ReactNode; colorB?: string}) => {
	const f = useCurrentFrame();
	const progress = interpolate(f, [4, 70], [0.02, 1], clamp);
	const all = [...a, ...b];
	const lo = Math.min(...all), hi = Math.max(...all);
	return (
		<Enter>
			<Title t={title} icon={icon} />
			<ChartFrame>
				<path d={path(a, lo, hi, progress)} fill="none" stroke={TEAL} strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" />
				<path d={path(b, lo, hi, progress)} fill="none" stroke={colorB} strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" />
			</ChartFrame>
			<Legend a={labelA} b={labelB} ca={TEAL} cb={colorB} />
			<Note t={note} />
		</Enter>
	);
};
export const DownLine = ({v, title, note}: {v: number[]; title: string; note: string}) => {
	const f = useCurrentFrame();
	const progress = interpolate(f, [4, 62], [0.02, 1], clamp);
	const first = v.slice(0, 12).reduce((x, y) => x + y) / 12;
	const last = v.slice(-10).reduce((x, y) => x + y) / 10;
	return (
		<Enter>
			<Title t={title} />
			<ChartFrame>
				<path d={path(v, 0, 105, progress)} fill="none" stroke={CORAL} strokeWidth={10} strokeLinejoin="round" strokeLinecap="round" />
			</ChartFrame>
			<div style={{position: 'absolute', left: 100, top: 345, fontSize: 38, fontWeight: 700, color: TEAL}}>2562 ≈ {Math.round(first)}</div>
			<div style={{position: 'absolute', right: 100, top: 345, fontSize: 38, fontWeight: 700, color: CORAL, opacity: progress > 0.9 ? 1 : 0}}>2569 ≈ {Math.round(last)}</div>
			<Note t={note} />
		</Enter>
	);
};
export const MonthBars = ({v, note}: {v: number[]; note: string}) => {
	const f = useCurrentFrame();
	const names = ['ม.ค.', '', 'มี.ค.', '', 'พ.ค.', '', 'ก.ค.', '', 'ก.ย.', '', 'พ.ย.', ''];
	const hi = Math.max(...v);
	return (
		<Enter>
			<Title t="คนค้น “ดูดวง” รายเดือน" />
			<ChartFrame>
				{v.map((y, i) => {
					const g = interpolate(f, [4 + i * 2, 22 + i * 2], [0, 1], clamp);
					const h = (y / hi) * 410 * g;
					return <g key={i}><rect x={105 + i * 73} y={840 - h} width={54} height={h} rx={10} fill={i ? '#c9c5b8' : CORAL} /><text x={132 + i * 73} y={885} textAnchor="middle" fontSize={26} fill={INK}>{names[i]}</text></g>;
				})}
				<g transform={`translate(${132} ${interpolate(f, [24, 42], [760, 395], clamp)})`} opacity={f > 24 ? 1 : 0}><path d="M0-52 40 2H16V50H-16V2H-40Z" fill={SUN} stroke={INK} strokeWidth={5} strokeLinejoin="round" /></g>
			</ChartFrame>
			<Note t={note} />
		</Enter>
	);
};

const Teller = () => {
	const f = useCurrentFrame();
	return (
		<g>
			<path d="M-170 250Q-170-30 0-40Q170-30 170 250Z" fill={PURPLE} />
			<path d="M-96-20Q-112-158 0-164Q112-158 96-20Q60-60 0-60Q-60-60-96-20Z" fill="#54319c" />
			<circle cy={-60} r={66} fill="#f2c7a5" />
			<path d="M-66-72Q0-118 66-72Q40-96 0-96Q-40-96-66-72Z" fill="#54319c" />
			<path d="M-34-62Q-24-52-14-62M14-62Q24-52 34-62" stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />
			<path d="M-14-30Q0-20 14-30" stroke="#c9505c" strokeWidth={6} fill="none" strokeLinecap="round" />
			<path d="M-60 130Q-30 90 -6 130M60 130Q30 90 6 130" stroke="#f2c7a5" strokeWidth={22} fill="none" strokeLinecap="round" transform={`translate(0 ${Math.sin(f * 0.1) * 5})`} />
			<Star x={0} y={-132} s={0.7} />
		</g>
	);
};
const Hexagram = () => {
	const f = useCurrentFrame();
	return <g transform={`rotate(${f * 1.2})`}><path d="M0-82 71 41H-71Z" fill="none" stroke={SUN} strokeWidth={9} /><path d="M0 82-71-41H71Z" fill="none" stroke={SUN} strokeWidth={9} /><circle r={16} fill={SUN} /></g>;
};
const Tarot = ({delay, face}: {delay: number; face: 'sun' | 'moon' | 'star'}) => {
	const f = useCurrentFrame();
	const t = interpolate(f, [delay, delay + 16], [0, 1], clamp);
	const sx = Math.abs(Math.cos(t * Math.PI));
	const front = t > 0.5;
	return (
		<g transform={`scale(${Math.max(sx, 0.04)} 1)`}>
			<rect x={-68} y={-110} width={136} height={220} rx={14} fill={front ? '#fff8e1' : '#3b2a7a'} stroke={SUN} strokeWidth={7} />
			{!front && <><Star x={0} y={0} s={1.4} /><path d="M-48-86H48M-48 86H48" stroke={SUN} strokeWidth={4} /></>}
			{front && face === 'sun' && <g>{Array.from({length: 8}, (_, i) => <path key={i} transform={`rotate(${i * 45})`} d="M-7-52 0-74 7-52Z" fill={CORAL} />)}<circle r={44} fill={SUN} stroke={CORAL} strokeWidth={4} /></g>}
			{front && face === 'moon' && <path d="M22-58A60 60 0 1 0 22 58A46 46 0 1 1 22-58Z" fill={PURPLE} />}
			{front && face === 'star' && <><Star x={0} y={-16} s={1.9} fill={TEAL} /><Star x={-34} y={58} s={0.6} fill={SUN} /><Star x={34} y={58} s={0.6} fill={SUN} /></>}
		</g>
	);
};
export const FortuneScene = () => {
	const f = useCurrentFrame();
	const glow = 0.55 + Math.sin(f * 0.18) * 0.25;
	return (
		<Stage top="#1f2159" bottom="#6d4aa8">
			{Array.from({length: 18}, (_, i) => <circle key={i} cx={(i * 163) % 1080} cy={40 + (i * 97) % 300} r={2 + (i % 3)} fill="#fff" opacity={0.4 + 0.5 * Math.abs(Math.sin(f * 0.08 + i))} />)}
			<Pop x={880} y={290}><Hexagram /></Pop>
			<Pop x={540} y={520}><g transform="scale(1.1)"><Teller /></g></Pop>
			<Pop x={160} y={480} delay={8}><Float phase={1}><g transform="rotate(-8)"><Tarot delay={18} face="sun" /></g></Float></Pop>
			<Pop x={920} y={560} delay={14}><Float phase={2}><g transform="rotate(8)"><Tarot delay={26} face="moon" /></g></Float></Pop>
			<Pop x={190} y={820} delay={20}><Float phase={3}><g transform="rotate(5) scale(.85)"><Tarot delay={34} face="star" /></g></Float></Pop>
			<rect x={250} y={920} width={580} height={36} rx={18} fill="#3b2a7a" />
			<Pop x={540} y={810} delay={4}>
				<circle r={150 + glow * 22} fill={SKY} opacity={0.22} />
				<circle r={138} fill="url(#ball)" stroke="#d9f3ff" strokeWidth={6} />
				<defs><radialGradient id="ball" cx="35%" cy="30%"><stop offset="0" stopColor="#fff" /><stop offset="0.45" stopColor={SKY} /><stop offset="1" stopColor={PURPLE} /></radialGradient></defs>
				<g opacity={glow}><Star x={0} y={0} s={2} /></g>
				<path d="M-90 124H90L118 160H-118Z" fill={SUN} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
			</Pop>
		</Stage>
	);
};
export const StatBadge = ({num, t}: {num: string; t: string}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = spring({frame: f, fps, config: {damping: 11, stiffness: 150}});
	return <div style={{position: 'absolute', left: 300, top: 140, padding: '12px 40px', borderRadius: 40, background: '#fff', textAlign: 'center', transform: `scale(${p})`, boxShadow: '0 10px 30px rgba(0,0,0,.3)'}}><div style={{fontSize: 74, fontWeight: 700, color: CORAL, lineHeight: 1.2}}>{num}</div><div style={{fontSize: 30, color: INK}}>{t}</div></div>;
};
export const CausationScene = () => {
	const f = useCurrentFrame();
	const wob = Math.sin(f * 0.14) * 14;
	return (
		<Stage top="#bdeaf8" bottom="#fff6dd" floor="#fff0c2">
			<Pop x={270} y={700}><circle cy={wob} r={130} fill={TEAL} /></Pop>
			<Pop x={810} y={700} delay={6}><circle cy={wob} r={130} fill={CORAL} /></Pop>
			<Pop x={540} y={700} delay={16}><text textAnchor="middle" y={62} fontSize={190} fontWeight={700} fill={INK}>≠</text></Pop>
		</Stage>
	);
};
export const SnoopScene = () => {
	const f = useCurrentFrame();
	const x = 300 + Math.sin(f * 0.07) * 240;
	return (
		<Stage top="#1f2159" bottom="#6d4aa8">
			{Array.from({length: 8}, (_, r) => Array.from({length: 12}, (_, c) => <rect key={`${r}${c}`} x={110 + c * 72} y={300 + r * 72} width={56} height={56} rx={10} fill={(r + c * 3) % 7 === 0 ? SUN : '#fff'} opacity={0.2 + ((r * 5 + c * 7) % 10) * 0.05} />))}
			<g transform={`translate(${x} 590)`}><circle r={150} fill={SKY} opacity={0.25} stroke="#fff" strokeWidth={16} /><path d="M108 108 200 200" stroke="#fff" strokeWidth={30} strokeLinecap="round" /></g>
		</Stage>
	);
};

type CatMode = 'coin' | 'detective' | 'shrug';
export const MemeCat = ({mode, text}: {mode: CatMode; text: string}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = spring({frame: f, fps, config: {damping: 10, stiffness: 170}});
	const lift = mode === 'shrug' ? Math.abs(Math.sin(f * 0.14)) * 22 : 0;
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
			<g transform={`translate(720 1590) scale(${p})`}>
				<path d="M-115-60L-130-170L-40-112ZM115-60L130-170L40-112Z" fill="#f2994a" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
				<ellipse rx={138} ry={120} fill="#f2994a" stroke={INK} strokeWidth={7} />
				{mode === 'coin' ? <><Coin x={-50} y={-16} r={38} /><Coin x={50} y={-16} r={38} /></> : <><circle cx={-50} cy={-16} r={24} fill="#fff" stroke={INK} strokeWidth={6} /><circle cx={50} cy={-16} r={24} fill="#fff" stroke={INK} strokeWidth={6} /><circle cx={mode === 'detective' ? -44 : -50} cy={-14} r={10} fill={INK} /><circle cx={mode === 'detective' ? 56 : 50} cy={-14} r={10} fill={INK} /></>}
				<path d="M-24 52Q0 72 24 52" stroke={INK} strokeWidth={7} fill="none" strokeLinecap="round" />
				<path d="M-100 28L-170 16M-100 48L-170 56M100 28L170 16M100 48L170 56" stroke={INK} strokeWidth={6} strokeLinecap="round" />
				{mode === 'detective' && <><path d="M-110-82Q0-170 110-82Q0-110-110-82Z" fill="#6b4a2c" stroke={INK} strokeWidth={6} /><g transform={`translate(${112 + Math.sin(f * 0.15) * 16} 58)`}><circle r={44} fill={SKY} opacity={0.55} stroke={INK} strokeWidth={9} /><path d="M32 32 76 76" stroke={INK} strokeWidth={14} strokeLinecap="round" /></g></>}
				{mode === 'shrug' && <path d={`M-136 ${58 - lift}Q-186 ${18 - lift}-214 ${-22 - lift}M136 ${58 - lift}Q186 ${18 - lift} 214 ${-22 - lift}`} stroke={INK} strokeWidth={15} fill="none" strokeLinecap="round" />}
				<text textAnchor="middle" y={-158} fontSize={62} fontWeight={700} fill={CORAL} stroke="#fff" strokeWidth={10} paintOrder="stroke">{text}</text>
			</g>
		</svg>
	);
};
