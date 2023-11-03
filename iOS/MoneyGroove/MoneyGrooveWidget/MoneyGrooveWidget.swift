//
//  MoneyGrooveWidget.swift
//  MoneyGrooveWidget
//
//  Created by Anders Hovmöller on 2023-10-28.
//

import WidgetKit
import SwiftUI

class Groove: Identifiable, Decodable {
    var today: Int
    var benchmark_by_date: [Int: Int]
}

func fetchGroove() async throws -> Groove? {
    let defaults = UserDefaults.init(suiteName: "group.moneygroove")!
    guard let username = defaults.string(forKey: "username") else { return nil }
    guard let password = defaults.string(forKey: "password") else { return nil }

    let url = URL(string: "https://moneygroove.kodare.com/api/v1/groove/")!
    
    var request = URLRequest(url: url)
    request.httpMethod = "GET"
    
    request.setValue(username, forHTTPHeaderField: "x-username")
    request.setValue(password, forHTTPHeaderField: "x-password")
    
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(Groove.self, from: data)
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), amount: nil, amountTomorrow: nil)
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> ()) {
        let entry = SimpleEntry(date: Date(), amount: nil, amountTomorrow: nil)
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        Task {
            guard let groove = try? await fetchGroove() else {
                return
            }
            let tomorrow = Calendar.current.date(byAdding: DateComponents(day: 1), to: Date())!
            let amountTomorrow = groove.benchmark_by_date[Calendar.current.component(.day, from: tomorrow)]

            let entries: [SimpleEntry] = [
                SimpleEntry(date: Calendar.current.date(byAdding: .hour, value: 1, to: Date())!, amount: groove.today, amountTomorrow: amountTomorrow)
            ]

            // Create the timeline with the entry and a reload policy with the date
            // for the next update.
            let timeline = Timeline(
                entries: entries,
                policy: .atEnd            )
            
            // Call the completion to pass the timeline to WidgetKit.
            completion(timeline)
        }
    }
}

struct SimpleEntry: TimelineEntry {
    var date: Date
    let amount: Int?
    let amountTomorrow: Int?
}

struct MoneyGrooveWidgetEntryView : View {
    var entry: Provider.Entry

    var body: some View {
        VStack {
            VStack {
                if let amount = entry.amount {
                    Text("\(amount)").font(.system(size: 30))

                    if let amount = entry.amountTomorrow {
                        Text("\(amount)").font(.system(size: 20))
                    }
                }
                else {
                    Text("...")
                }
            }
        }
    }
}

struct MoneyGrooveWidget: Widget {
    let kind: String = "MoneyGrooveWidget"
    var urlSession: URLSession? = nil

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            if #available(iOS 17.0, *) {
                MoneyGrooveWidgetEntryView(entry: entry)
                    .containerBackground(.fill.tertiary, for: .widget)
            } else {
                MoneyGrooveWidgetEntryView(entry: entry)
                    .padding()
                    .background()
            }
        }
        .configurationDisplayName("Money Groove Widget")
//        .description("")
    }
}

#Preview(as: .systemSmall) {
    MoneyGrooveWidget()
} timeline: {
    SimpleEntry(date: .now, amount: 31234, amountTomorrow: 30134)
}
