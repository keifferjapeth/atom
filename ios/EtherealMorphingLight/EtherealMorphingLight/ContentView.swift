import SwiftUI

struct ContentView: View {
    var body: some View {
        GeometryReader { geometry in
            let width = geometry.size.width
            let height = geometry.size.height
            let isCompactHeight = height < 720

            ZStack {
                Color.black
                    .ignoresSafeArea()

                AnimatedNebulaBackground()
                    .ignoresSafeArea()

                EnergyHaloOverlay()
                    .ignoresSafeArea()

                Group {
                    if isCompactHeight {
                        ScrollView(showsIndicators: false) {
                            heroContent(width: width, height: height)
                        }
                    } else {
                        heroContent(width: width, height: height)
                    }
                }
            }
            .frame(width: width, height: height)
        }
    }

    @ViewBuilder
    private func heroContent(width: CGFloat, height: CGFloat) -> some View {
        let horizontalInset = max(18, min(32, width * 0.07))
        let verticalInset = max(28, min(52, height * 0.08))
        let stackSpacing = max(18, min(34, height * 0.045))
        let cardPadding = EdgeInsets(
            top: max(24, verticalInset * 0.55),
            leading: max(22, horizontalInset * 0.75),
            bottom: max(24, verticalInset * 0.55),
            trailing: max(22, horizontalInset * 0.75)
        )
        let heroScale = min(1.2, max(0.78, width / 430))
        let skillSpacing = max(12, min(18, height * 0.024))
        let textSpacing = max(16, min(24, height * 0.03))
        let headerSpacing = max(6, min(12, height * 0.015))
        let cardMaxWidth = min(520, width - horizontalInset * 2)
        let topSpacer = height > 860 ? height * 0.08 : height * 0.04

        VStack(spacing: stackSpacing) {
            Spacer(minLength: topSpacer)

            GlassCard {
                VStack(spacing: textSpacing) {
                    VStack(spacing: headerSpacing) {
                        Text("Jarvis Sentinel Uplink")
                            .font(.system(size: max(22, min(28, width * 0.065)), weight: .semibold, design: .rounded))
                            .foregroundStyle(Color.white.opacity(0.95))
                            .multilineTextAlignment(.center)

                        Text("Seamless cognition anchor priming hero-grade protocols.")
                            .font(.system(size: max(14, min(17, width * 0.04)), weight: .medium, design: .rounded))
                            .foregroundStyle(Color.white.opacity(0.75))
                            .multilineTextAlignment(.center)
                            .lineSpacing(4)
                    }

                    SuperpowerGlyphField(scale: heroScale)
                        .padding(.top, max(8, textSpacing * 0.4))

                    VStack(spacing: skillSpacing) {
                        JarvisSkillRow(
                            icon: "bolt.fill",
                            title: "Photon Forecast",
                            detail: "Predictive energy routing 4.7s ahead",
                            layoutWidth: cardMaxWidth
                        )

                        JarvisSkillRow(
                            icon: "waveform.path.ecg",
                            title: "Vital Shield",
                            detail: "Autonomous resilience sweep every 900ms",
                            layoutWidth: cardMaxWidth
                        )

                        JarvisSkillRow(
                            icon: "antenna.radiowaves.left.and.right",
                            title: "Quantum Link",
                            detail: "Jarvis neural uplink stabilized at 99.98%",
                            layoutWidth: cardMaxWidth
                        )
                    }

                    VoiceCommandWaveform()
                        .padding(.top, max(4, textSpacing * 0.25))
                }
                .padding(cardPadding)
            }
            .frame(maxWidth: cardMaxWidth)
            .padding(.horizontal, horizontalInset)

            CommandOrbField(maxWidth: width, scale: heroScale)

            PlaceholderFooter()
                .padding(.bottom, max(0, verticalInset * 0.35))
        }
        .padding(.horizontal, horizontalInset)
        .padding(.vertical, verticalInset)
        .frame(maxWidth: .infinity)
        .frame(minHeight: height)
    }
}

#Preview {
    ContentView()
}
