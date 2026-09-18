export default function RaceCar({ width = 260 }) {
  return (
    <div className="race-car-wrap" style={{ width }}>
      <svg
        className="race-car-svg"
        viewBox="0 8 420 128"
        role="img"
        aria-label="Animated F1 car, 2022+ generation body"
      >
        <defs>
          <linearGradient id="bodyGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#ff4a3d" />
            <stop offset="50%" stopColor="#e10600" />
            <stop offset="100%" stopColor="#7a0000" />
          </linearGradient>
          <linearGradient id="wingGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#232329" />
            <stop offset="100%" stopColor="#08080a" />
          </linearGradient>
          <radialGradient id="tireShine" cx="35%" cy="28%" r="72%">
            <stop offset="0%" stopColor="#75757f" />
            <stop offset="100%" stopColor="#18181c" />
          </radialGradient>
          <linearGradient id="visorGradient" x1="0" y1="0" x2="1" y2="0.4">
            <stop offset="0%" stopColor="#40404a" />
            <stop offset="100%" stopColor="#050507" />
          </linearGradient>
          <linearGradient id="floorGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#0a0a0e" />
            <stop offset="100%" stopColor="#000" />
          </linearGradient>
          <filter id="carGlow" x="-20%" y="-40%" width="140%" height="180%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#e10600" floodOpacity="0.45" />
          </filter>
        </defs>

        {/* speed lines / motion trail */}
        <g className="speed-lines" stroke="#e10600" strokeLinecap="round" opacity="0.55">
          <line x1="2" y1="66" x2="30" y2="66" strokeWidth="3" />
          <line x1="0" y1="82" x2="24" y2="82" strokeWidth="2.5" />
          <line x1="6" y1="98" x2="28" y2="98" strokeWidth="2" />
        </g>

        <g className="car-body-group" filter="url(#carGlow)">
          {/* rear wing: wide, tall, mounted high (2022+ reg) */}
          <rect x="26" y="26" width="7" height="9" rx="1.5" fill="url(#wingGradient)" />
          <rect x="14" y="24" width="26" height="6" rx="1.5" fill="#151519" />
          <rect x="18" y="30" width="18" height="4" rx="1" fill="#e10600" opacity="0.6" />
          <rect x="26" y="35" width="6" height="30" fill="url(#wingGradient)" />

          {/* rear crash structure / engine cover taper */}
          <path d="M32 60 L60 52 L60 90 L32 96 Z" fill="url(#bodyGradient)" />

          {/* floor / diffuser (ground effect, 2022+) */}
          <path d="M48 92 L200 100 L230 100 L230 108 L190 108 L48 100 Z" fill="url(#floorGradient)" />
          <path d="M56 94 L90 97 L88 104 L54 101 Z" fill="#1c1c22" />
          <path d="M96 97 L130 99 L128 106 L94 104 Z" fill="#1c1c22" />

          {/* rear wheel - large 18in-proportioned */}
          <g className="wheel-spin">
            <circle cx="66" cy="96" r="30" fill="url(#tireShine)" />
            <circle cx="66" cy="96" r="30" fill="none" stroke="#4a4a54" strokeWidth="2" />
            <circle cx="66" cy="96" r="14" fill="#dcdce0" />
            <circle cx="66" cy="96" r="14" fill="none" stroke="#8a8a90" strokeWidth="1" />
            {[0, 51.4, 102.8, 154.2, 205.6, 257, 308.4].map((deg) => (
              <line
                key={deg}
                x1="66"
                y1="96"
                x2={66 + 11.5 * Math.cos((deg * Math.PI) / 180)}
                y2={96 + 11.5 * Math.sin((deg * Math.PI) / 180)}
                stroke="#9a9aa0"
                strokeWidth="2.4"
              />
            ))}
            <circle cx="66" cy="96" r="3.5" fill="#2c2c32" />
          </g>

          {/* main sculpted body: low nose-to-cockpit taper, wide sidepod shoulders */}
          <path
            d="M56 74
               C60 54 78 42 108 39
               C136 36 168 36 196 40
               L252 48
               C270 50 288 54 302 60
               L302 78
               C288 82 270 84 252 85
               L196 88
               C168 90 136 90 108 87
               C78 84 60 92 56 74 Z"
            fill="url(#bodyGradient)"
          />

          {/* sidepod undercut shading (post-2022: clean, no bargeboards) */}
          <path d="M118 44 L198 46 L196 82 L114 80 Z" fill="#5c0000" opacity="0.5" />
          <path d="M122 48 L188 50 L186 55 L120 53 Z" fill="#ffb3ac" opacity="0.3" />
          <path d="M118 74 C130 82 160 86 190 84 L190 88 C160 90 128 87 116 79 Z" fill="#3a0000" opacity="0.6" />

          {/* engine cover spine highlight */}
          <path d="M196 40 L252 48 L250 53 L194 46 Z" fill="#ffffff" opacity="0.1" />

          {/* halo, mounted above cockpit per 2018+ safety reg */}
          <path
            d="M204 41 C212 22 246 19 262 34 L264 46"
            stroke="#1c1c22"
            strokeWidth="7"
            fill="none"
            strokeLinecap="round"
          />
          <path
            d="M204 41 C212 22 246 19 262 34 L264 46"
            stroke="#e10600"
            strokeWidth="2.5"
            fill="none"
            strokeLinecap="round"
          />
          {/* halo center pylon */}
          <line x1="232" y1="26" x2="230" y2="42" stroke="#1c1c22" strokeWidth="4" strokeLinecap="round" />

          {/* cockpit opening + driver helmet hint */}
          <path d="M210 40 C220 30 242 29 254 38 L256 47 L212 48 Z" fill="url(#visorGradient)" />
          <circle cx="232" cy="40" r="6" fill="#0a0a0f" stroke="#2a2a30" strokeWidth="1" />

          {/* front wing flush-mounted to nose (2022+ reg: no gap) */}
          <path
            d="M302 60
               C316 60 328 62 340 65
               L340 73
               C328 76 316 78 302 78 Z"
            fill="url(#bodyGradient)"
          />
          <rect x="338" y="55" width="5" height="28" rx="1.5" fill="url(#wingGradient)" />
          <path d="M334 58 L400 65 L400 68 L334 66 Z" fill="url(#wingGradient)" />
          <path d="M334 70 L400 70 L400 73 L334 72 Z" fill="url(#wingGradient)" />
          <path d="M334 74 L396 78 L396 81 L334 78 Z" fill="url(#wingGradient)" />
          <rect x="396" y="60" width="4" height="24" rx="1" fill="#151519" />
          <path d="M340 68 L352 70 L340 72 Z" fill="#e10600" />

          {/* front wheel - large 18in-proportioned */}
          <g className="wheel-spin">
            <circle cx="330" cy="96" r="27" fill="url(#tireShine)" />
            <circle cx="330" cy="96" r="27" fill="none" stroke="#4a4a54" strokeWidth="2" />
            <circle cx="330" cy="96" r="12.5" fill="#dcdce0" />
            <circle cx="330" cy="96" r="12.5" fill="none" stroke="#8a8a90" strokeWidth="1" />
            {[0, 51.4, 102.8, 154.2, 205.6, 257, 308.4].map((deg) => (
              <line
                key={deg}
                x1="330"
                y1="96"
                x2={330 + 10 * Math.cos((deg * Math.PI) / 180)}
                y2={96 + 10 * Math.sin((deg * Math.PI) / 180)}
                stroke="#9a9aa0"
                strokeWidth="2.2"
              />
            ))}
            <circle cx="330" cy="96" r="3" fill="#2c2c32" />
          </g>

          {/* number roundel */}
          <circle cx="220" cy="62" r="11" fill="#0a0a0f" stroke="#fff" strokeWidth="1.5" />
          <text
            x="220"
            y="66.5"
            fontSize="12"
            fontWeight="800"
            fill="#fff"
            textAnchor="middle"
            fontFamily="'Titillium Web', sans-serif"
          >
            1
          </text>
        </g>
      </svg>
    </div>
  );
}
