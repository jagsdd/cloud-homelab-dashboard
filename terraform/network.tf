resource "aws_vpc" "homelab" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "cloud-homelab-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.homelab.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = true

  tags = {
    Name = "cloud-homelab-public-subnet"
  }
}

resource "aws_internet_gateway" "homelab" {
  vpc_id = aws_vpc.homelab.id

  tags = {
    Name = "cloud-homelab-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.homelab.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.homelab.id
  }

  tags = {
    Name = "cloud-homelab-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "ec2" {
  name        = "cloud-homelab-ec2"
  description = "Security group for cloud homelab EC2 instance"
  vpc_id      = aws_vpc.homelab.id

  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["81.110.200.122/32"]
  }

  ingress {
    description = "HTTP from the internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from the internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "cloud-homelab-ec2"
  }
}

resource "aws_key_pair" "homelab" {
  key_name   = "cloud-homelab-key"
  public_key = file("/home/jagsd/.ssh/id_ed25519.pub")

  tags = {
    Name = "cloud-homelab-key"
  }
}

resource "aws_instance" "homelab" {
  ami           = "ami-03cf5768bcc686a8c"
  instance_type = "t3.small"
  subnet_id     = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.ec2.id
  ]

  key_name = aws_key_pair.homelab.key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name = "cloud-homelab-server"
  }
}