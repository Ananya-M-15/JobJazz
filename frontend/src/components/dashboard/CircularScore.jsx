export default function CircularScore({ score }) {
  const radius = 60;
  const stroke = 8;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const colorClass = score >= 75 ? "text-emerald-500" : score >= 50 ? "text-amber-500" : "text-rose-500";

  return (
    <div className="relative flex items-center justify-center">
      <svg
        height={radius * 2}
        width={radius * 2}
        className="-rotate-90 transform"
        aria-label="Match score circle"
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
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          className={`${colorClass}`}
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center text-center">
        <span className={`text-3xl font-bold ${colorClass}`}>{score}%</span>
        <span className="text-[10px] font-semibold uppercase tracking-widest text-slate-400 mt-0.5">Match</span>
      </div>
    </div>
  );
}
