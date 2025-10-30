import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            AnimatedNebulaBackground()
                .ignoresSafeArea()
            VStack(spacing: 32) {
                Spacer()
                GlassCard {
                    VStack(spacing: 16) {
                        Text("Ethereal Cognition Placeholder")
                            .font(.system(size: 24, weight: .semibold, design: .rounded))
                            .foregroundStyle(Color.white.opacity(0.9))
                            .multilineTextAlignment(.center)

                        Text("An aurora of intuition gathers before the AI awakens.")
                            .font(.system(size: 16, weight: .medium, design: .rounded))
                            .foregroundStyle(Color.white.opacity(0.75))
                            .multilineTextAlignment(.center)
                            .lineSpacing(4)

                        HStack(spacing: 12) {
                            PulsingLightDot(delay: 0)
                            PulsingLightDot(delay: 0.3)
                            PulsingLightDot(delay: 0.6)
                        }
                        .padding(.top, 4)
                    }
                    .padding(24)
                }
                .padding(.horizontal, 24)

                Spacer()
                PlaceholderFooter()
            }
            .padding(.vertical, 48)
        }
    }
}

#Preview {
    ContentView()
}
