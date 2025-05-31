export default function ContactComponent(
    {
        contact,
        setContact
    }:
    {
        contact: string;
        setContact: (contact: string) => void;
    }
)
{
    return (
        <div>
            <input
                type="tel"
                placeholder="enter your phone number"
                value={contact}
                onChange={(e) => setContact(e.target.value)}
            />
        </div>
    );
}