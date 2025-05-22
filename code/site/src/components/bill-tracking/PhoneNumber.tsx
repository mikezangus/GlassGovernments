export default function PhoneNumberComponent({
    phoneNumber,
    setPhoneNumber
}: {
    phoneNumber: string;
    setPhoneNumber: (phone: string) => void;
})
{
    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <span>Phone number</span>
            <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
            />
        </div>
    );
}
