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
    var size: CGFloat = 18

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
                    endRadius: size
                )
            )
            .frame(width: size, height: size)
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
    var scale: CGFloat = 1.0
    @State private var auraPulse: CGFloat = 0.2

    var body: some View {
        let clampedScale = min(1.25, max(0.72, scale))
        let haloSize = 180 * clampedScale
        let ringBase = 110 * clampedScale
        let titleSize = max(16, min(22, 18 * clampedScale))
        let subtitleSize = max(12, min(15, 13 * clampedScale))
        let dotSize = max(12, min(18, 16 * clampedScale))

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
                        startRadius: 12 * clampedScale,
                        endRadius: haloSize
                    )
                )
                .frame(width: haloSize, height: haloSize)

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
                    .frame(
                        width: CGFloat(ringBase + CGFloat(index) * 22 * clampedScale),
                        height: CGFloat(ringBase + CGFloat(index) * 22 * clampedScale)
                    )
                    .rotationEffect(.degrees(Double(index) * 24 + Double(auraPulse) * 120))
                    .opacity(0.35 - Double(index) * 0.06)
            }

            VStack(spacing: 8 * clampedScale) {
                Text("Prime Aegis")
                    .font(.system(size: titleSize, weight: .semibold, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.9))

                HStack(spacing: 8 * clampedScale) {
                    ForEach(0..<3) { index in
                        PulsingLightDot(delay: Double(index) * 0.25, size: dotSize)
                    }
                }

                Text("Heroic resonance 87% charged")
                    .font(.system(size: subtitleSize, weight: .medium, design: .rounded))
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
    var layoutWidth: CGFloat

    var body: some View {
        let isCompact = layoutWidth < 360
        let titleSize = isCompact ? 15 : 16
        let detailSize = isCompact ? 12.5 : 13.5
        let iconSize: CGFloat = isCompact ? 16 : 18
        let iconFrame: CGFloat = isCompact ? 32 : 36

        HStack(alignment: .top, spacing: isCompact ? 12 : 14) {
            Image(systemName: icon)
                .font(.system(size: iconSize, weight: .semibold))
                .foregroundStyle(Color.cyan.opacity(0.85))
                .frame(width: iconFrame, height: iconFrame)
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
                    .font(.system(size: CGFloat(titleSize), weight: .semibold, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.9))

                Text(detail)
                    .font(.system(size: CGFloat(detailSize), weight: .medium, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.62))
                    .lineSpacing(isCompact ? 2 : 3)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            Capsule()
                .fill(
                    LinearGradient(
                        colors: [Color.cyan.opacity(0.15), Color.purple.opacity(0.05)],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: isCompact ? 44 : 46, height: isCompact ? 16 : 18)
                .overlay(
                    Text("ON")
                        .font(.system(size: isCompact ? 10.5 : 11, weight: .bold, design: .rounded))
                        .foregroundStyle(Color.white.opacity(0.8))
                )
        }
        .padding(isCompact ? 12 : 14)
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
                .stroke(
                    LinearGradient(
                        colors: [Color.white.opacity(0.0), Color.cyan.opacity(0.2)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 1
                )
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
                    let step = max(1, size.width / 60)
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
    let maxWidth: CGFloat
    let scale: CGFloat
    var contentInsets: EdgeInsets? = nil

    var body: some View {
        let orbScale = min(1.15, max(0.8, scale * 0.95))
        let spacing = max(18, min(32, maxWidth * 0.08))
        let orbSizeEstimate = 72 * min(1.2, max(0.82, scale * 0.95)) + max(12, min(18, orbScale * 12))
        let tripleThreshold = max(520, orbSizeEstimate * 3 + spacing * 1.8)
        let doubleThreshold = max(380, orbSizeEstimate * 2 + spacing * 1.2)
        let insets = contentInsets ?? EdgeInsets(
            top: max(12, min(24, maxWidth * 0.04)),
            leading: max(16, min(28, maxWidth * 0.08)),
            bottom: max(10, min(20, maxWidth * 0.035)),
            trailing: max(16, min(28, maxWidth * 0.08))
        )

        Group {
            if maxWidth >= tripleThreshold {
                HStack(spacing: spacing) {
                    ForEach(0..<3) { index in
                        orb(for: index, scale: orbScale)
                    }
                }
                .frame(maxWidth: .infinity)
            } else if maxWidth >= doubleThreshold {
                VStack(spacing: spacing) {
                    HStack(spacing: spacing) {
                        orb(for: 0, scale: orbScale)
                        orb(for: 1, scale: orbScale)
                    }
                    .frame(maxWidth: .infinity)

                    HStack(spacing: spacing) {
                        orb(for: 2, scale: orbScale)
                    }
                    .frame(maxWidth: .infinity)
                }
                .frame(maxWidth: .infinity)
            } else {
                VStack(spacing: spacing) {
                    ForEach(0..<3) { index in
                        orb(for: index, scale: orbScale)
                    }
                }
                .frame(maxWidth: .infinity)
            }
        }
        .padding(.top, insets.top)
        .padding(.bottom, insets.bottom)
        .padding(.leading, insets.leading)
        .padding(.trailing, insets.trailing)
    }

    @ViewBuilder
    private func orb(for index: Int, scale: CGFloat) -> some View {
        CommandOrb(
            title: index == 0 ? "Shield" : index == 1 ? "Scan" : "Deploy",
            subtitle: index == 0 ? "Impact deflect" : index == 1 ? "Spectral sweep" : "Nanite swarm",
            delay: Double(index) * 0.35,
            scale: scale
        )
    }
}

private struct CommandOrb: View {
    let title: String
    let subtitle: String
    let delay: Double
    let scale: CGFloat
    @State private var animate = false

    var body: some View {
        let clampedScale = min(1.2, max(0.82, scale))
        let orbSize = 72 * clampedScale
        let titleSize = max(12, min(14, 13 * clampedScale))
        let subtitleSize = max(10, min(12, 11 * clampedScale))

        VStack(spacing: 8 * clampedScale) {
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color.cyan.opacity(0.45),
                            Color.purple.opacity(0.35),
                            Color.blue.opacity(0.05)
                        ],
                        center: .center,
                        startRadius: 6 * clampedScale,
                        endRadius: orbSize
                    )
                )
                .overlay(
                    Circle()
                        .stroke(Color.white.opacity(0.3), lineWidth: 1.5)
                )
                .overlay(
                    Image(systemName: "sparkles")
                        .font(.system(size: 18 * clampedScale, weight: .semibold))
                        .foregroundStyle(Color.white.opacity(0.9))
                )
                .frame(width: orbSize, height: orbSize)
                .scaleEffect(animate ? 1.08 : 0.96)
                .shadow(color: Color.cyan.opacity(0.4), radius: 18, x: 0, y: 10)

            VStack(spacing: 2 * clampedScale) {
                Text(title)
                    .font(.system(size: titleSize, weight: .semibold, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.85))

                Text(subtitle)
                    .font(.system(size: subtitleSize, weight: .medium, design: .rounded))
                    .foregroundStyle(Color.white.opacity(0.55))
            }
        }
        .padding(.vertical, 8 * clampedScale)
        .padding(.horizontal, 6 * clampedScale)
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

struct CommandOrbConsole: View {
    let availableWidth: CGFloat
    let scale: CGFloat

    var body: some View {
        let headingSize = max(16, min(20, availableWidth * 0.06))
        let detailSize = max(12, min(14, availableWidth * 0.045))
        let sectionSpacing = max(14, min(22, availableWidth * 0.05))
        let detailSpacing = max(6, min(12, availableWidth * 0.03))
        let horizontalPadding = max(20, min(30, availableWidth * 0.08))
        let topPadding = max(22, min(34, availableWidth * 0.09))
        let bottomPadding = max(18, min(28, availableWidth * 0.07))

        GlassCard {
            VStack(alignment: .leading, spacing: sectionSpacing) {
                VStack(alignment: .leading, spacing: detailSpacing) {
                    Text("Command Matrix")
                        .font(.system(size: headingSize, weight: .semibold, design: .rounded))
                        .foregroundStyle(Color.white.opacity(0.92))

                    Text("Orbital directives online")
                        .font(.system(size: detailSize, weight: .medium, design: .rounded))
                        .foregroundStyle(Color.white.opacity(0.6))
                }

                CommandOrbField(
                    maxWidth: availableWidth,
                    scale: scale,
                    contentInsets: EdgeInsets(
                        top: sectionSpacing * 0.45,
                        leading: 0,
                        bottom: sectionSpacing * 0.3,
                        trailing: 0
                    )
                )
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.top, topPadding)
            .padding(.bottom, bottomPadding)
            .padding(.horizontal, horizontalPadding)
        }
    }
}
