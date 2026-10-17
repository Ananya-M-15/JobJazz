export default function CircularScore({ score }) {
  const displayScore = Math.round(score);
  const radius = 64;
  const stroke = 7;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const clampedScore = Math.min(100, Math.max(0, displayScore));
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  const colorClass = displayScore >= 75 ? "text-emerald-500" : displayScore >= 50 ? "text-amber-500" : "text-rose-500";

  return (
    <div className="relative flex items-center justify-center shrink-0">
      <svg
        height={radius * 2}
        width={radius * 2}
        className="-rotate-90 transform"
        aria-label={`Match score circle: ${displayScore}%`}
      >
        <circle
          stroke="#f1f5f9" /* slate-100 */
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke="currentColor"
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={circumference + " " + circumference}
          style={{ strokeDashoffset, transition: "stroke-dashoffset 1s ease-in-out" }}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          className={`${colorClass}`}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center select-none pointer-events-none">
        <span className={`text-2xl sm:text-3xl font-extrabold tracking-tight ${colorClass}`}>
          {displayScore}%
        </span>
        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 -mt-0.5">
          Match
        </span>
      </div>
    </div>
  );
}
