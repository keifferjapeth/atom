import SwiftUI

struct AnimatedNebulaBackground: View {
    @State private var baseHue: Double = Double.random(in: 0...1)

    var body: some View {
        TimelineView(.animation) { timeline in
            Canvas { context, size in
                let time = timeline.date.timeIntervalSinceReferenceDate
                let center = CGPoint(x: size.width / 2, y: size.height / 2)

                context.blendMode = .plusLighter

                for index in 0..<6 {
                    let progression = time / 6 + Double(index)
                    let angle = progression.truncatingRemainder(dividingBy: .pi * 2)
                    let radius = size.width * 0.3 + sin(progression * 1.7) * size.width * 0.15

                    let position = CGPoint(
                        x: center.x + cos(angle) * radius,
                        y: center.y + sin(angle * 0.9) * radius
                    )

                    let blobSize = size.width * 0.65 + cos(time / 2 + Double(index)) * size.width * 0.1
                    let rect = CGRect(
                        x: position.x - blobSize / 2,
                        y: position.y - blobSize / 2,
                        width: blobSize,
                        height: blobSize
                    )

                    let hueOffset = (baseHue + Double(index) * 0.12 + sin(time / 5) * 0.1)
                        .truncatingRemainder(dividingBy: 1)

                    let gradient = Gradient(colors: [
                        Color(hue: hueOffset, saturation: 0.85, brightness: 1).opacity(0.6),
                        Color(hue: (hueOffset + 0.12).truncatingRemainder(dividingBy: 1), saturation: 0.75, brightness: 0.8).opacity(0.35),
                        Color.black.opacity(0)
                    ])

                    context.fill(
                        Path(ellipseIn: rect),
                        with: .radialGradient(
                            gradient,
                            center: UnitPoint(
                                x: position.x / size.width,
                                y: position.y / size.height
                            ),
                            startRadius: blobSize * 0.1,
                            endRadius: blobSize * 0.6
                        )
                    )
                }

                let ringCount = 5
                for ringIndex in 0..<ringCount {
                    let progress = (Double(ringIndex) / Double(ringCount))
                    let ringRadius = size.width * 0.3 + CGFloat(progress) * size.width * 0.45

                    var path = Path()
                    path.addEllipse(in: CGRect(
                        x: center.x - ringRadius,
                        y: center.y - ringRadius,
                        width: ringRadius * 2,
                        height: ringRadius * 2
                    ))

                    let opacity = 0.12 - progress * 0.02 + sin(time * 0.8 + Double(ringIndex)) * 0.02

                    context.stroke(path, with: .color(Color.white.opacity(opacity)), lineWidth: 2.5)
                }
            }
        }
        .blur(radius: 65)
        .brightness(0.08)
        .task {
            withAnimation(.easeInOut(duration: 20).repeatForever(autoreverses: true)) {
                baseHue = Double.random(in: 0...1)
            }
        }
    }
}

struct GlassCard<Content: View>: View {
    @ViewBuilder let content: Content

    var body: some View {
        RoundedRectangle(cornerRadius: 32, style: .continuous)
            .fill(.ultraThinMaterial)
            .overlay(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .stroke(
                        LinearGradient(
                            colors: [
                                Color.white.opacity(0.4),
                                Color.white.opacity(0.1)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1
                    )
            )
            .shadow(color: Color.black.opacity(0.35), radius: 24, x: 0, y: 18)
            .overlay(
                content
            )
    }
}

struct PulsingLightDot: View {
    @State private var animate = false
    let delay: Double

    var body: some View {
        Circle()
            .fill(
                RadialGradient(
                    colors: [
                        Color.white.opacity(0.9),
                        Color.white.opacity(0.2)
                    ],
                    center: .center,
                    startRadius: 0,
                    endRadius: 16
                )
            )
            .frame(width: 18, height: 18)
            .scaleEffect(animate ? 1.4 : 0.8)
            .opacity(animate ? 1 : 0.35)
            .animation(
                .easeInOut(duration: 1.6)
                    .repeatForever()
                    .delay(delay),
                value: animate
            )
            .onAppear {
                animate = true
            }
    }
}

struct PlaceholderFooter: View {
    @State private var shimmerPhase: CGFloat = 0

    var body: some View {
        VStack(spacing: 12) {
            Text("Intelligence calibrating")
                .font(.system(size: 14, weight: .medium, design: .rounded))
                .foregroundStyle(Color.white.opacity(0.65))
                .overlay(alignment: .leading) {
                    GeometryReader { proxy in
                        let width = proxy.size.width
                        Rectangle()
                            .fill(
                                LinearGradient(
                                    colors: [
                                        Color.white.opacity(0),
                                        Color.white.opacity(0.7),
                                        Color.white.opacity(0)
                                    ],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .frame(width: width * 0.35)
                            .offset(x: width * shimmerPhase)
                    }
                    .mask(alignment: .leading) {
                        Text("Intelligence calibrating")
                            .font(.system(size: 14, weight: .medium, design: .rounded))
                    }
                }

            Capsule()
                .fill(Color.white.opacity(0.15))
                .frame(width: 160, height: 6)
                .overlay(
                    Capsule()
                        .fill(
                            LinearGradient(
                                colors: [
                                    Color.white.opacity(0.1),
                                    Color.white.opacity(0.6),
                                    Color.white.opacity(0.1)
                                ],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .frame(width: 80)
                        .offset(x: 80 * shimmerPhase)
                )
        }
        .padding(.bottom, 24)
        .task {
            withAnimation(
                .easeInOut(duration: 2.4)
                    .repeatForever(autoreverses: false)
            ) {
                shimmerPhase = 1
            }
        }
    }
}

struct EnergyHaloOverlay: View {
    var body: some View {
        TimelineView(.animation) { timeline in
            Canvas { context, size in
                let time = timeline.date.timeIntervalSinceReferenceDate
                let baseRadius = min(size.width, size.height) * 0.35
                let center = CGPoint(x: size.width / 2, y: size.height / 2)

                for orbit in 0..<3 {
                    let progress = time * (0.15 + Double(orbit) * 0.05)
                    let radius = baseRadius + CGFloat(orbit) * baseRadius * 0.18
                    let dashPhase = CGFloat(progress.truncatingRemainder(dividingBy: 1)) * 360

                    var path = Path()
                    path.addEllipse(in: CGRect(
                        x: center.x - radius,
                        y: center.y - radius,
                        width: radius * 2,
                        height: radius * 2
                    ))

                    let gradientColor = Color(
                        hue: (0.55 + Double(orbit) * 0.08).truncatingRemainder(dividingBy: 1),
                        saturation: 0.7,
                        brightness: 1
                    )

                    context.stroke(
                        path,
                        with: .linearGradient(
                            Gradient(colors: [
                                gradientColor.opacity(0.25),
                                Color.white.opacity(0.1),
                                gradientColor.opacity(0.35)
                            ]),
                            startPoint: CGPoint(x: center.x - radius, y: center.y - radius),
                            endPoint: CGPoint(x: center.x + radius, y: center.y + radius)
                        ),
                        style: StrokeStyle(lineWidth: 3.5, lineCap: .round, dash: [18, 26], dashPhase: dashPhase)
                    )
                }

                for spark in 0..<36 {
                    let harmonic = sin(time * 0.45 + Double(spark) * 0.33)
                    let orbitRadius = baseRadius * (0.82 + harmonic * 0.12 + Double(spark) * 0.004)
                    let angle = Double(spark) / 36.0 * .pi * 2 + time * 0.35
                    let point = CGPoint(
                        x: center.x + CGFloat(cos(angle)) * orbitRadius,
                        y: center.y + CGFloat(sin(angle)) * orbitRadius
                    )

                    let sparkSize: CGFloat = 3.2 + CGFloat(sin(time + Double(spark))) * 1.2
                    let opacity = 0.25 + sin(time * 1.2 + Double(spark)) * 0.2
                    let sparkRect = CGRect(
                        x: point.x - sparkSize / 2,
                        y: point.y - sparkSize / 2,
                        width: sparkSize,
                        height: sparkSize
                    )

                    context.fill(
                        Path(ellipseIn: sparkRect),
                        with: .color(Color.white.opacity(opacity))
                    )
                }
            }
        }
        .blur(radius: 12)
        .opacity(0.9)
        .allowsHitTesting(false)
    }
}

struct SuperpowerGlyphField: View {
    @State private var auraPulse: CGFloat = 0.2

    var body: some View {
        ZStack {
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color.white.opacity(0.14),
                            Color.blue.opacity(0.05),
                            Color.clear
                        ],
                        center: .center,
                        startRadius: 12,
                        endRadius: 110
                    )
                )
                .frame(width: 180, height: 180)

            ForEach(0..<4) { index in
                Circle()
                    .stroke(
                        AngularGradient(
                            gradient: Gradient(colors: [
                                Color.cyan.opacity(0.1),
                                Color.white.opacity(0.45),
                                Color.purple.opacity(0.25),
                                Color.cyan.opacity(0.1)
                            ]),
                            center: .center,
                            startAngle: .degrees(0),
                            endAngle: .degrees(360)
                        ),
                        lineWidth: CGFloat(2 + index)
                    )
                    .frame(width: CGFloat(110 + index * 22), height: CGFloat(110 + index * 22))
                    .rotationEffect(.degrees(Double(index) * 24 + Double(auraPulse) * 120))
                    .opacity(0.35 - Double(index) * 0.06)
            }

            VStack(spacing: 8) {
                Text("Prime Aegis")
                    .font(.system(size: 18, weight: .semibold, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.9))

                HStack(spacing: 8) {
                    ForEach(0..<3) { index in
                        PulsingLightDot(delay: Double(index) * 0.25)
                    }
                }

                Text("Heroic resonance 87% charged")
                    .font(.system(size: 13, weight: .medium, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.6))
            }
        }
        .frame(maxWidth: .infinity)
        .task {
            withAnimation(.easeInOut(duration: 3).repeatForever(autoreverses: true)) {
                auraPulse = 1
            }
        }
    }
}

struct JarvisSkillRow: View {
    let icon: String
    let title: String
    let detail: String

    var body: some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(.system(size: 18, weight: .semibold))
                .foregroundStyle(Color.cyan.opacity(0.85))
                .frame(width: 36, height: 36)
                .background(
                    Circle()
                        .fill(Color.white.opacity(0.08))
                        .overlay(
                            Circle()
                                .stroke(Color.white.opacity(0.18), lineWidth: 1)
                        )
                        .shadow(color: Color.cyan.opacity(0.45), radius: 12, x: 0, y: 6)
                )

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.system(size: 16, weight: .semibold, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.9))

                Text(detail)
                    .font(.system(size: 13.5, weight: .medium, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.62))
                    .lineLimit(2)
            }

            Spacer()

            Capsule()
                .fill(
                    LinearGradient(
                        colors: [Color.cyan.opacity(0.15), Color.purple.opacity(0.05)],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: 46, height: 18)
                .overlay(
                    Text("ON")
                        .font(.system(size: 11, weight: .bold, design: .rounded))
                        .foregroundStyle(Color.white.opacity(0.8))
                )
        }
        .padding(14)
        .background(
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .fill(Color.white.opacity(0.05))
                .overlay(
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .stroke(Color.white.opacity(0.08), lineWidth: 1)
                )
        )
        .overlay(
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .stroke(LinearGradient(colors: [Color.white.opacity(0.0), Color.cyan.opacity(0.2)], startPoint: .topLeading, endPoint: .bottomTrailing), lineWidth: 1)
        )
    }
}

struct VoiceCommandWaveform: View {
    var body: some View {
        TimelineView(.animation) { timeline in
            let time = timeline.date.timeIntervalSinceReferenceDate
            Canvas { context, size in
                let midY = size.height / 2
                let amplitude = size.height * 0.28
                let path = Path { path in
                    let step = size.width / 60
                    path.move(to: CGPoint(x: 0, y: midY))
                    for x in stride(from: 0, through: size.width, by: step) {
                        let relative = x / size.width
                        let envelope = sin(.pi * relative)
                        let y = midY + sin(relative * 6 * .pi + CGFloat(time) * 3) * amplitude * envelope
                        path.addLine(to: CGPoint(x: x, y: y))
                    }
                }

                context.stroke(
                    path,
                    with: .linearGradient(
                        Gradient(colors: [
                            Color.cyan.opacity(0.05),
                            Color.white.opacity(0.8),
                            Color.purple.opacity(0.05)
                        ]),
                        startPoint: CGPoint(x: 0, y: midY - amplitude),
                        endPoint: CGPoint(x: size.width, y: midY + amplitude)
                    ),
                    style: StrokeStyle(lineWidth: 2.4, lineCap: .round, lineJoin: .round)
                )
            }
            .frame(height: 48)
            .overlay(
                Text("Awaiting heroic command…")
                    .font(.system(size: 12, weight: .medium, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.6))
                    .offset(y: 24)
            )
        }
        .frame(height: 64)
    }
}

struct CommandOrbField: View {
    var body: some View {
        HStack(spacing: 28) {
            ForEach(0..<3) { index in
                CommandOrb(
                    title: index == 0 ? "Shield" : index == 1 ? "Scan" : "Deploy",
                    subtitle: index == 0 ? "Impact deflect" : index == 1 ? "Spectral sweep" : "Nanite swarm",
                    delay: Double(index) * 0.35
                )
            }
        }
        .padding(.horizontal, 24)
        .padding(.top, 8)
    }
}

private struct CommandOrb: View {
    let title: String
    let subtitle: String
    let delay: Double
    @State private var animate = false

    var body: some View {
        VStack(spacing: 8) {
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color.cyan.opacity(0.45),
                            Color.purple.opacity(0.35),
                            Color.blue.opacity(0.05)
                        ],
                        center: .center,
                        startRadius: 6,
                        endRadius: 70
                    )
                )
                .overlay(
                    Circle()
                        .stroke(Color.white.opacity(0.3), lineWidth: 1.5)
                )
                .overlay(
                    Image(systemName: "sparkles")
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundStyle(Color.white.opacity(0.9))
                )
                .frame(width: 72, height: 72)
                .scaleEffect(animate ? 1.08 : 0.96)
                .shadow(color: Color.cyan.opacity(0.4), radius: 18, x: 0, y: 10)

            VStack(spacing: 2) {
                Text(title)
                    .font(.system(size: 13, weight: .semibold, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.85))

                Text(subtitle)
                    .font(.system(size: 11, weight: .medium, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.55))
            }
        }
        .padding(.vertical, 8)
        .onAppear {
            withAnimation(
                .easeInOut(duration: 2)
                    .delay(delay)
                    .repeatForever(autoreverses: true)
            ) {
                animate = true
            }
        }
    }
}
