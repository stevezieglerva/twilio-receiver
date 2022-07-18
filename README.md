# twilio-receiver


Software Architecture

``` mermaid
graph TD;

    twilio[Twilio]
    clock[[Clock]]
    repo[S3 Repo]



    twilio-->IProcessingTexts
    IProcessingTexts-->ReminderProcessor
    clock-->IGettingTime
    IGettingTime-->ReminderProcessor
    repo-->IStoringReminders
    IStoringReminders-->ReminderProcessor

    IProcessingTexts-->SMSCommandProcessor
    IGettingTime-->SMSCommandProcessor
    IStoringReminders-->SMSCommandProcessor

    twilio-->CommandAdapter-->SMSCommandProcessor

    Cron-->SendAdapter-->ReminderProcessor


    subgraph Hex
        subgraph Domain
            ReminderProcessor
            SMSCommandProcessor
        end
        subgraph Adapters
            CommandAdapter
            SendAdapter
        end
        IProcessingTexts
        IGettingTime
        IStoringReminders
        CommandAdapter
        SendAdapter


    end
```