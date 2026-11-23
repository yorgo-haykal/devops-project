# Deliberate misconfiguration to check that the security scan fails.
resource "aws_security_group" "open" {
  name        = "open-to-world"
  description = "Deliberately insecure"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
