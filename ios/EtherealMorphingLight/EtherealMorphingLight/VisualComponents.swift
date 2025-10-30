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
