import { ContactType } from "@/lib/types";


function ChooseContactTypeComponent(
    {
        contactType,
        setContactType
    }:
    {
        contactType: ContactType;
        setContactType: (contactType: ContactType) => void;
    }
)
{
    return (
        <div>
            <label htmlFor="contact-type-select">Preferred contact method:</label>
            <select
                id="contact-type-select"
                value={contactType}
                onChange={(e) => setContactType(e.target.value as ContactType)}
            >
                <option value={ContactType.Telegram}>Telegram</option>
                <option value={ContactType.Text}>Text</option>
            </select>
        </div>
    );
}


function InputPhoneNumberComponent(
    {
        contactValue,
        setContactValue
    }:
    {
        contactValue: string;
        setContactValue: (contactValue: string) => void;
    }
)
{
    return (
        <div>
            <input
                type="tel"
                placeholder="enter your phone number"
                value={contactValue}
                onChange={(e) => setContactValue(e.target.value)}
            />
        </div>
    );
}


export default function ContactComponent(
    {
        contactType,
        setContactType,
        contactValue,
        setContactValue
    }:
    {
        contactType: ContactType;
        setContactType: (contactType: ContactType) => void;
        contactValue: string;
        setContactValue: (contactValue: string) => void;
    }
)
{
    return (
        <div>
            <ChooseContactTypeComponent
                contactType={contactType}
                setContactType={setContactType}
            />
            {contactType === ContactType.Telegram && (
                <div>Telegram</div>
            )}
            {contactType === ContactType.Text && (
                <InputPhoneNumberComponent
                    contactValue={contactValue}
                    setContactValue={setContactValue}
                />
            )}
        </div>
    );
}
