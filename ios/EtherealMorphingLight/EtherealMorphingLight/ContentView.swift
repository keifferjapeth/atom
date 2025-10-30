import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()

            AnimatedNebulaBackground()
                .ignoresSafeArea()

            EnergyHaloOverlay()
                .ignoresSafeArea()

            VStack(spacing: 32) {
                Spacer(minLength: 24)

                GlassCard {
                    VStack(spacing: 20) {
                        VStack(spacing: 8) {
                            Text("Jarvis Sentinel Uplink")
                                .font(.system(size: 26, weight: .semibold, design: .rounded))
                                .foregroundStyle(Color.white.opacity(0.95))

                            Text("Seamless cognition anchor priming hero-grade protocols.")
                                .font(.system(size: 16, weight: .medium, design: .rounded))
                                .foregroundStyle(Color.white.opacity(0.75))
                                .multilineTextAlignment(.center)
                                .lineSpacing(4)
                        }

                        SuperpowerGlyphField()
                            .padding(.top, 12)

                        VStack(spacing: 14) {
                            JarvisSkillRow(
                                icon: "bolt.fill",
                                title: "Photon Forecast",
                                detail: "Predictive energy routing 4.7s ahead"
                            )

                            JarvisSkillRow(
                                icon: "waveform.path.ecg",
                                title: "Vital Shield",
                                detail: "Autonomous resilience sweep every 900ms"
                            )

                            JarvisSkillRow(
                                icon: "antenna.radiowaves.left.and.right",
                                title: "Quantum Link",
                                detail: "Jarvis neural uplink stabilized at 99.98%"
                            )
                        }

                        VoiceCommandWaveform()
                            .padding(.top, 6)
                    }
                    .padding(.horizontal, 26)
                    .padding(.vertical, 28)
                }
                .padding(.horizontal, 24)

                CommandOrbField()

                PlaceholderFooter()
            }
            .padding(.vertical, 48)
            .padding(.horizontal, 12)
        }
    }
}

#Preview {
    ContentView()
}
