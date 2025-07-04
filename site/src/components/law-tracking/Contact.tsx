import { ContactMethod } from "@/lib/types";


function ChooseContactTypeComponent(
    {
        contactType,
        setContactType
    }:
    {
        contactType: ContactMethod;
        setContactType: (contactType: ContactMethod) => void;
    }
)
{
    return (
        <div>
            <label htmlFor="contact-type-select">Preferred contact method:</label>
            <select
                id="contact-type-select"
                value={contactType}
                onChange={(e) => setContactType(e.target.value as ContactMethod)}
            >
                <option value={ContactMethod.Telegram}>Telegram</option>
                <option value={ContactMethod.Text}>Text</option>
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
        contactType: ContactMethod;
        setContactType: (contactType: ContactMethod) => void;
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
            {contactType === ContactMethod.Telegram && (
                <div>Telegram</div>
            )}
            {contactType === ContactMethod.Text && (
                <InputPhoneNumberComponent
                    contactValue={contactValue}
                    setContactValue={setContactValue}
                />
            )}
        </div>
    );
}
