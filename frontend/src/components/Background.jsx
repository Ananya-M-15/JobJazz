export default function Background() {
    return (
        <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none" aria-hidden="true">
            <div className="absolute inset-0 bg-slate-50" />
            
            {/* Primary Curve - Upper Right */}
            <div 
                className="absolute w-[50rem] h-[50rem] rounded-full bg-indigo-100 opacity-30 blur-[100px]"
                style={{
                    top: '-15%',
                    right: '-10%',
                }}
            />
            
            {/* Secondary Curve - Lower Left */}
            <div 
                className="absolute w-[40rem] h-[40rem] rounded-full bg-blue-50 opacity-40 blur-3xl"
                style={{
                    bottom: '-15%',
                    left: '-10%',
                }}
            />
        </div>
    );
}